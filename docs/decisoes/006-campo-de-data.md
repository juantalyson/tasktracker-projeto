# 006. Campo de data do site com máscara e calendário

**Data:** 19/10/2026 · **Status:** aceita

## Contexto
No formulário do site era preciso digitar as barras da data (`DD/MM/AAAA`) à mão, e não
havia como consultar os dias do mês.

## Decisão
- **Máscara:** as barras entram sozinhas enquanto a pessoa digita (`25102026` → `25/10/2026`).
- **Calendário opcional:** um botão 📅 ao lado do campo abre o calendário do navegador e
  preenche a data no formato `DD/MM/AAAA`.
- Também foi colocada uma logo ao lado do nome "tasktracker" no topo do site.

## Consequências
- ✅ Menos erro de digitação e uma forma rápida de escolher o dia.
- ✅ A validação continua no servidor (`tarefas.py`): a regra é a mesma do terminal.
- ⚠️ Vale só para o site. No terminal, o `input()` só recebe o texto depois do Enter, então lá a data continua sendo digitada com as barras.
