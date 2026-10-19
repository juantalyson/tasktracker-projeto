"""Acesso ao banco de dados (SQLite).

O SQLite é um banco que fica num único arquivo e já vem com o Python.
O terminal e o site usam este mesmo arquivo, então uma tarefa cadastrada
em um lugar aparece no outro.
"""

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

# Pasta do projeto (um nível acima de src/)
PASTA_PROJETO = Path(__file__).resolve().parent.parent

# O caminho pode ser trocado pela variável de ambiente TASKTRACKER_DB (usada no Docker)
CAMINHO_PADRAO = PASTA_PROJETO / "dados" / "tasktracker.db"


def _caminho():
    return Path(os.environ.get("TASKTRACKER_DB", CAMINHO_PADRAO))


@contextmanager
def conectar():
    """Abre o banco, cria a tabela se ainda não existir, e fecha no final."""
    caminho = _caminho()
    caminho.parent.mkdir(parents=True, exist_ok=True)
    conexao = sqlite3.connect(caminho)
    conexao.row_factory = sqlite3.Row  # permite ler as colunas pelo nome
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS tarefas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo      TEXT NOT NULL,
            descricao   TEXT NOT NULL DEFAULT '',
            prioridade  TEXT NOT NULL,
            data_limite TEXT NOT NULL,
            status      TEXT NOT NULL DEFAULT 'Pendente'
        )
        """
    )
    try:
        yield conexao
        conexao.commit()
    finally:
        conexao.close()


def salvar(tarefa):
    """Grava uma tarefa nova e devolve ela com o id gerado."""
    with conectar() as conexao:
        cursor = conexao.execute(
            "INSERT INTO tarefas (titulo, descricao, prioridade, data_limite, status) "
            "VALUES (?, ?, ?, ?, ?)",
            (tarefa["titulo"], tarefa["descricao"], tarefa["prioridade"],
             tarefa["data_limite"], tarefa["status"]),
        )
        return {"id": cursor.lastrowid, **tarefa}


def listar():
    """Todas as tarefas, na ordem em que foram cadastradas."""
    with conectar() as conexao:
        linhas = conexao.execute("SELECT * FROM tarefas ORDER BY id").fetchall()
    return [dict(linha) for linha in linhas]


def buscar(id_tarefa):
    with conectar() as conexao:
        linha = conexao.execute("SELECT * FROM tarefas WHERE id = ?", (id_tarefa,)).fetchone()
    return dict(linha) if linha else None


def mudar_status(id_tarefa, status):
    """Muda o status. Devolve a tarefa atualizada, ou None se o id não existir."""
    with conectar() as conexao:
        conexao.execute("UPDATE tarefas SET status = ? WHERE id = ?", (status, id_tarefa))
    return buscar(id_tarefa)
