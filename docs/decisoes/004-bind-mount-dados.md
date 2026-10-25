# 004. Banco na pasta `dados/` do projeto (bind mount)

**Data:** 19/10/2026 · **Status:** aceita (substitui o volume nomeado `tasktracker-data`)

## Contexto
No começo, o `docker-compose.yml` guardava o banco num **volume nomeado** do Docker
(`tasktracker-data`), como previsto no planejamento da Fase 1. Esse volume não aparece
como pasta no Windows, então não dava para abrir o banco no VS Code. E, rodando sem
Docker (`python src/main.py`), o programa usava outro banco, separado do Docker.

## Decisão
Trocar o volume nomeado por um **bind mount**: `./dados:/app/dados`, nos serviços
`tasktracker-app` e `web`. A pasta `dados/` do projeto passa a ser a mesma pasta do
banco dentro do container.

## Consequências
- ✅ O Docker e o Python no Windows usam **o mesmo** `dados/tasktracker.db`.
- ✅ Dá para abrir o banco direto no VS Code (extensão SQLite Viewer).
- ✅ As tarefas continuam salvas depois do `--rm`, como antes.
- ⚠️ É diferente do texto do planejamento da Fase 1, que fala em "volume do Docker". O bind mount também é uma forma de volume, mas usa uma pasta do computador.
- ⚠️ O `docker run -it --rm tasktracker` (sem `-v`) continua sem guardar os dados. Isso é esperado no modo isolado.
