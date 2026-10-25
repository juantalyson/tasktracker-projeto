# Decisões do projeto

Registro curto das principais decisões técnicas do TaskTracker: o que foi decidido e por quê.
Cada arquivo segue o mesmo modelo: **Contexto** (o problema), **Decisão** (o que fizemos)
e **Consequências** (o que ganhamos e o que perdemos).

| # | Decisão | Data |
|---|---|---|
| 001 | [Regras de negócio num só arquivo (`tarefas.py`)](001-regras-centralizadas.md) | 19/10/2026 |
| 002 | [SQLite para guardar as tarefas](002-sqlite.md) | 19/10/2026 |
| 003 | [Imagem `python:3.11-slim` e ordem das camadas](003-imagem-docker.md) | 19/10/2026 |
| 004 | [Banco na pasta `dados/` do projeto (bind mount)](004-bind-mount-dados.md) | 19/10/2026 |
| 005 | [Fuso horário de Brasília no container](005-fuso-horario.md) | 19/10/2026 |
| 006 | [Campo de data do site com máscara e calendário](006-campo-de-data.md) | 19/10/2026 |
