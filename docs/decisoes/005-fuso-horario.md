# 005. Fuso horário de Brasília no container

**Data:** 19/10/2026 · **Status:** aceita

## Contexto
O container usa o horário **UTC**, 3 horas à frente de Brasília. Entre 21h e meia-noite,
o container já achava que era o dia seguinte, e os textos "vence hoje" e "atrasada"
saíam errados. Na auditoria, o container mostrava 22:51 quando eram 19:51.

## Decisão
Adicionar `ENV TZ=America/Sao_Paulo` no `Dockerfile`.

## Consequências
- ✅ O cálculo de prazos usa o dia certo em qualquer horário.
- ✅ A data de "Hoje" no painel web bate com a do computador.
- ⚠️ O fuso fica fixo em Brasília. Para outro lugar, basta trocar o `TZ` (ex.: `docker run -e TZ=...`).
