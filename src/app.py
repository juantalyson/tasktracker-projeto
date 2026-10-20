"""TaskTracker: site e API (Flask).

Usa as mesmas regras (tarefas.py) e o mesmo banco (banco.py) do terminal.

Como rodar:  python src/app.py   e abrir http://localhost:8000
"""

import os
from datetime import date

from flask import Flask, jsonify, render_template, request

import banco
import tarefas

app = Flask(__name__, template_folder="web/templates", static_folder="web/static")
app.json.ensure_ascii = False  # mostra "Média" em vez de "Média" no JSON
app.json.sort_keys = False


def com_prazo(tarefa):
    """Acrescenta à tarefa os campos calculados que o site mostra."""
    return {
        **tarefa,
        "data_limite_br": tarefas.data_br(tarefa["data_limite"]),
        "prazo": tarefas.texto_prazo(tarefa),
        "atrasada": tarefas.esta_atrasada(tarefa),
    }


def erro(campo, mensagem, codigo):
    return jsonify({"erro": {"campo": campo, "mensagem": mensagem}}), codigo


# ---------- Páginas ----------

@app.get("/")
def pagina_inicial():
    return render_template("index.html")


@app.get("/docs")
def pagina_docs():
    return render_template("docs.html")


# ---------- API ----------

@app.get("/saude")
def saude():
    return jsonify({"status": "ok"})


@app.get("/tarefas")
def listar_tarefas():
    """Lista as tarefas, ordenadas pela data limite. Filtros opcionais: ?prioridade=Alta&status=Pendente"""
    lista = banco.listar()

    prioridade = request.args.get("prioridade")
    if prioridade:
        try:
            prioridade = tarefas.validar_prioridade(prioridade)
        except tarefas.ErroValidacao as e:
            return erro(e.campo, e.mensagem, 422)
        lista = [t for t in lista if t["prioridade"] == prioridade]

    status = request.args.get("status")
    if status:
        lista = [t for t in lista if t["status"].lower() == status.lower()]

    lista.sort(key=lambda t: (t["data_limite"], t["id"]))
    return jsonify([com_prazo(t) for t in lista])


@app.post("/tarefas")
def cadastrar_tarefa():
    """Cadastra uma tarefa com as mesmas validações do terminal."""
    dados = request.get_json(silent=True) or {}
    try:
        tarefa = tarefas.nova_tarefa(
            dados.get("titulo"),
            dados.get("descricao"),
            dados.get("prioridade"),
            dados.get("data_limite"),
        )
    except tarefas.ErroValidacao as e:
        return erro(e.campo, e.mensagem, 422)
    return jsonify(com_prazo(banco.salvar(tarefa))), 201


@app.patch("/tarefas/<int:id_tarefa>/concluir")
def concluir_tarefa(id_tarefa):
    tarefa = banco.mudar_status(id_tarefa, tarefas.STATUS_CONCLUIDA)
    if tarefa is None:
        return erro("id", f"Erro: tarefa {id_tarefa} não encontrada.", 404)
    return jsonify(com_prazo(tarefa))


@app.get("/estatisticas")
def estatisticas():
    """Totais para a visão geral + os próximos prazos pendentes."""
    lista = banco.listar()
    pendentes = sorted(
        (t for t in lista if t["status"] == tarefas.STATUS_PENDENTE),
        key=lambda t: t["data_limite"],
    )
    return jsonify({
        **tarefas.estatisticas(lista),
        "hoje": date.today().strftime("%d/%m/%Y"),
        "proximos_prazos": [com_prazo(t) for t in pendentes[:5]],
    })


if __name__ == "__main__":
    # 0.0.0.0 = aceita conexões de fora do container (necessário no Docker)
    porta = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=porta, debug=os.environ.get("FLASK_DEBUG") == "1")
