"""Regras de negócio do TaskTracker.

Este arquivo é o "coração" do sistema: as validações e cálculos ficam aqui
para que o terminal (main.py) e o site (app.py) sigam exatamente as mesmas regras.
"""

import unicodedata
from datetime import date, datetime

PRIORIDADES = ["Alta", "Média", "Baixa"]
STATUS_PENDENTE = "Pendente"
STATUS_CONCLUIDA = "Concluída"

ERRO_TITULO = "Erro: o título não pode ficar vazio."
ERRO_PRIORIDADE = "Erro: prioridade inválida. Use Alta, Média ou Baixa."
ERRO_DATA = "Erro: data inválida. Use DD/MM/AAAA com uma data real."


class ErroValidacao(Exception):
    """Erro de regra de negócio. Guarda o campo e a mensagem para o usuário."""

    def __init__(self, campo, mensagem):
        super().__init__(mensagem)
        self.campo = campo
        self.mensagem = mensagem


def _sem_acento(texto):
    """'Média' -> 'media'. Usado para comparar a prioridade digitada."""
    normalizado = unicodedata.normalize("NFD", texto)
    return "".join(c for c in normalizado if unicodedata.category(c) != "Mn").lower()


def validar_titulo(texto):
    """Título obrigatório: rejeita vazio ou só espaços."""
    titulo = (texto or "").strip()
    if not titulo:
        raise ErroValidacao("titulo", ERRO_TITULO)
    return titulo


def validar_prioridade(texto):
    """Aceita só Alta, Média (ou Media) e Baixa, sem diferenciar maiúsculas."""
    digitado = _sem_acento((texto or "").strip())
    for prioridade in PRIORIDADES:
        if digitado == _sem_acento(prioridade):
            return prioridade
    raise ErroValidacao("prioridade", ERRO_PRIORIDADE)


def validar_data(texto):
    """Data limite no formato DD/MM/AAAA e que exista de verdade (31/02 é recusada).

    Devolve um objeto date.
    """
    try:
        return datetime.strptime((texto or "").strip(), "%d/%m/%Y").date()
    except ValueError:
        raise ErroValidacao("data_limite", ERRO_DATA) from None


def nova_tarefa(titulo, descricao, prioridade, data_limite):
    """Valida tudo e monta o dicionário da tarefa. Status começa como Pendente."""
    return {
        "titulo": validar_titulo(titulo),
        "descricao": (descricao or "").strip(),
        "prioridade": validar_prioridade(prioridade),
        "data_limite": validar_data(data_limite).isoformat(),  # guardada como AAAA-MM-DD
        "status": STATUS_PENDENTE,
    }


def data_br(data_iso):
    """'2026-10-20' -> '20/10/2026'."""
    return date.fromisoformat(data_iso).strftime("%d/%m/%Y")


def dias_restantes(tarefa, hoje=None):
    """Quantos dias faltam para a data limite (negativo = atrasada)."""
    hoje = hoje or date.today()
    return (date.fromisoformat(tarefa["data_limite"]) - hoje).days


def esta_atrasada(tarefa, hoje=None):
    return tarefa["status"] == STATUS_PENDENTE and dias_restantes(tarefa, hoje) < 0


def texto_prazo(tarefa, hoje=None):
    """Frase curta sobre o prazo, mostrada no terminal e no site."""
    if tarefa["status"] != STATUS_PENDENTE:
        return "—"
    dias = dias_restantes(tarefa, hoje)
    if dias < 0:
        return f"atrasada há {-dias} dia" + ("s" if dias < -1 else "")
    if dias == 0:
        return "vence hoje"
    return f"vence em {dias} dia" + ("s" if dias > 1 else "")


def estatisticas(lista, hoje=None):
    """Totais usados no rodapé do terminal e na visão geral do site."""
    hoje = hoje or date.today()
    pendentes = [t for t in lista if t["status"] == STATUS_PENDENTE]
    concluidas = [t for t in lista if t["status"] == STATUS_CONCLUIDA]
    atrasadas = [t for t in pendentes if dias_restantes(t, hoje) < 0]
    proximos_7 = [t for t in pendentes if 0 <= dias_restantes(t, hoje) <= 7]

    por_prioridade = {}
    for prioridade in PRIORIDADES:
        da_prioridade = [t for t in lista if t["prioridade"] == prioridade]
        por_prioridade[prioridade] = {
            "total": len(da_prioridade),
            "pendentes": sum(1 for t in da_prioridade if t["status"] == STATUS_PENDENTE),
            "concluidas": sum(1 for t in da_prioridade if t["status"] == STATUS_CONCLUIDA),
        }

    return {
        "total": len(lista),
        "pendentes": len(pendentes),
        "concluidas": len(concluidas),
        "percentual_concluidas": round(100 * len(concluidas) / len(lista)) if lista else 0,
        "atrasadas": len(atrasadas),
        "vencem_em_7_dias": len(proximos_7),
        "por_prioridade": por_prioridade,
    }
