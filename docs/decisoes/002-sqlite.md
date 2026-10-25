# 002. SQLite para guardar as tarefas

**Data:** 19/10/2026 · **Status:** aceita

## Contexto
Na primeira versão as tarefas ficavam numa lista na memória e sumiam ao fechar o
programa. O terminal e o site também precisavam enxergar os mesmos dados.

## Decisão
Usar o **SQLite**, por meio de `src/banco.py`. O banco é um único arquivo
(`dados/tasktracker.db`), e a tabela `tarefas` é criada sozinha na primeira execução.
O caminho pode ser trocado pela variável `TASKTRACKER_DB`.

## Consequências
- ✅ Já vem com o Python: não precisa instalar nem configurar um servidor de banco.
- ✅ As tarefas continuam salvas depois de fechar o programa.
- ✅ O terminal e o site leem o mesmo arquivo.
- ⚠️ Serve para um usuário ou poucos. Para muitos acessos ao mesmo tempo, o ideal seria um banco servidor (ex.: PostgreSQL).
- ⚠️ O arquivo `.db` não vai para o Git (`.gitignore`): cada pessoa tem o seu.
