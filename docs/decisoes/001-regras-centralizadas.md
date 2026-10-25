# 001. Regras de negócio num só arquivo (`tarefas.py`)

**Data:** 19/10/2026 · **Status:** aceita

## Contexto
O sistema tem duas entradas: o menu do terminal (`main.py`) e o site (`app.py`).
Se cada uma tivesse as suas validações, uma regra poderia mudar num lugar e ficar
diferente no outro.

## Decisão
Todas as regras ficam em `src/tarefas.py`: validação de título, prioridade e data,
status inicial "Pendente" e o cálculo de prazos e totais. O terminal e o site só
chamam essas funções.

## Consequências
- ✅ A regra muda em um lugar só e vale para os dois.
- ✅ Dá para testar as regras sozinhas (`tests/test_tarefas.py`).
- ⚠️ O `main.py` deixou de ter todo o código num arquivo só, como no começo da Fase 2.
