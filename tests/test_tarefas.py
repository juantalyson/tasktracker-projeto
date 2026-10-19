"""Testes das regras do TaskTracker.

Como rodar (na pasta do projeto):  python -m unittest discover -s tests -v
"""

import os
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

# Deixa o Python achar os arquivos da pasta src/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import banco  # noqa: E402
import tarefas  # noqa: E402

HOJE = date(2026, 10, 18)


class TestValidacoes(unittest.TestCase):
    def test_titulo_vazio_ou_so_espacos_e_recusado(self):
        for texto in ["", "   ", None]:
            with self.assertRaises(tarefas.ErroValidacao):
                tarefas.validar_titulo(texto)

    def test_titulo_valido_perde_espacos_das_pontas(self):
        self.assertEqual(tarefas.validar_titulo("  Estudar Docker "), "Estudar Docker")

    def test_prioridades_aceitas(self):
        casos = {"Alta": "Alta", "alta": "Alta", "Média": "Média", "Media": "Média",
                 "media": "Média", "BAIXA": "Baixa", " Baixa ": "Baixa"}
        for digitado, esperado in casos.items():
            self.assertEqual(tarefas.validar_prioridade(digitado), esperado)

    def test_prioridade_invalida_e_recusada(self):
        for texto in ["urgente", "", "1", "Altaa"]:
            with self.assertRaises(tarefas.ErroValidacao) as contexto:
                tarefas.validar_prioridade(texto)
            self.assertEqual(contexto.exception.mensagem, tarefas.ERRO_PRIORIDADE)

    def test_data_valida(self):
        self.assertEqual(tarefas.validar_data("20/10/2026"), date(2026, 10, 20))

    def test_data_invalida_e_recusada(self):
        for texto in ["31/02/2026", "2026-10-20", "amanhã", "", "20/13/2026"]:
            with self.assertRaises(tarefas.ErroValidacao):
                tarefas.validar_data(texto)

    def test_nova_tarefa_comeca_pendente(self):
        tarefa = tarefas.nova_tarefa("Título", "", "alta", "20/10/2026")
        self.assertEqual(tarefa["status"], "Pendente")
        self.assertEqual(tarefa["data_limite"], "2026-10-20")


class TestPrazos(unittest.TestCase):
    def tarefa(self, data_iso, status="Pendente"):
        return {"data_limite": data_iso, "status": status, "prioridade": "Alta"}

    def test_textos_de_prazo(self):
        self.assertEqual(tarefas.texto_prazo(self.tarefa("2026-10-17"), HOJE), "atrasada há 1 dia")
        self.assertEqual(tarefas.texto_prazo(self.tarefa("2026-10-15"), HOJE), "atrasada há 3 dias")
        self.assertEqual(tarefas.texto_prazo(self.tarefa("2026-10-18"), HOJE), "vence hoje")
        self.assertEqual(tarefas.texto_prazo(self.tarefa("2026-10-19"), HOJE), "vence em 1 dia")
        self.assertEqual(tarefas.texto_prazo(self.tarefa("2026-10-20"), HOJE), "vence em 2 dias")
        self.assertEqual(tarefas.texto_prazo(self.tarefa("2026-10-01", "Concluída"), HOJE), "—")

    def test_estatisticas(self):
        lista = [
            self.tarefa("2026-10-17"),
            self.tarefa("2026-10-20"),
            self.tarefa("2026-10-01", "Concluída"),
        ]
        numeros = tarefas.estatisticas(lista, HOJE)
        self.assertEqual(numeros["total"], 3)
        self.assertEqual(numeros["pendentes"], 2)
        self.assertEqual(numeros["concluidas"], 1)
        self.assertEqual(numeros["atrasadas"], 1)
        self.assertEqual(numeros["vencem_em_7_dias"], 1)
        self.assertEqual(numeros["percentual_concluidas"], 33)

    def test_estatisticas_de_lista_vazia(self):
        self.assertEqual(tarefas.estatisticas([], HOJE)["percentual_concluidas"], 0)


class TestBanco(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        os.environ["TASKTRACKER_DB"] = os.path.join(self.pasta.name, "teste.db")

    def tearDown(self):
        del os.environ["TASKTRACKER_DB"]
        self.pasta.cleanup()

    def test_salvar_listar_e_concluir(self):
        self.assertEqual(banco.listar(), [])
        salva = banco.salvar(tarefas.nova_tarefa("Estudar", "volumes", "Baixa", "20/10/2026"))
        self.assertEqual(salva["id"], 1)
        self.assertEqual([t["titulo"] for t in banco.listar()], ["Estudar"])

        concluida = banco.mudar_status(1, tarefas.STATUS_CONCLUIDA)
        self.assertEqual(concluida["status"], "Concluída")
        self.assertIsNone(banco.mudar_status(99, tarefas.STATUS_CONCLUIDA))


try:
    import flask  # noqa: F401
except ImportError:
    flask = None


@unittest.skipIf(flask is None, "Flask não instalado (pip install -r requirements.txt)")
class TestApi(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        os.environ["TASKTRACKER_DB"] = os.path.join(self.pasta.name, "teste.db")
        from app import app
        self.cliente = app.test_client()

    def tearDown(self):
        del os.environ["TASKTRACKER_DB"]
        self.pasta.cleanup()

    def test_fluxo_completo(self):
        self.assertEqual(self.cliente.get("/saude").get_json(), {"status": "ok"})
        self.assertEqual(self.cliente.get("/tarefas").get_json(), [])

        resposta = self.cliente.post("/tarefas", json={
            "titulo": "API", "descricao": "", "prioridade": "media", "data_limite": "20/10/2026"})
        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(resposta.get_json()["prioridade"], "Média")
        self.assertEqual(resposta.get_json()["status"], "Pendente")

        resposta = self.cliente.patch("/tarefas/1/concluir")
        self.assertEqual(resposta.get_json()["status"], "Concluída")
        self.assertEqual(self.cliente.patch("/tarefas/99/concluir").status_code, 404)

        self.assertEqual(self.cliente.get("/estatisticas").get_json()["concluidas"], 1)
        self.assertEqual(self.cliente.get("/").status_code, 200)
        self.assertEqual(self.cliente.get("/docs").status_code, 200)

    def test_erros_de_validacao_respondem_422(self):
        casos = [
            ({"titulo": "  ", "prioridade": "Alta", "data_limite": "20/10/2026"}, "titulo"),
            ({"titulo": "X", "prioridade": "urgente", "data_limite": "20/10/2026"}, "prioridade"),
            ({"titulo": "X", "prioridade": "Alta", "data_limite": "31/02/2026"}, "data_limite"),
        ]
        for corpo, campo in casos:
            resposta = self.cliente.post("/tarefas", json=corpo)
            self.assertEqual(resposta.status_code, 422)
            self.assertEqual(resposta.get_json()["erro"]["campo"], campo)


if __name__ == "__main__":
    unittest.main()
