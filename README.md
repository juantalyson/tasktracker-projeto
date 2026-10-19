# TaskTracker

Gerenciador de tarefas no terminal, feito em Python 3.

Projeto do **Bootcamp II**: [SEU NOME COMPLETO], [SEU CURSO], polo [ASA NORTE ou TAGUATINGA].

## Descrição

Muita gente perde prazos porque anota as tarefas em lugares diferentes, ou nem anota.
O TaskTracker reúne tudo num lugar só: você cadastra a tarefa com título, descrição,
prioridade e data limite, e depois vê a lista completa no terminal.

### Funcionalidades

- Menu contínuo com 3 opções: cadastrar tarefa, visualizar tarefas e sair.
- Cada tarefa tem **título**, **descrição**, **prioridade**, **data limite** e **status**.
- O status começa sempre como **Pendente**.
- Mensagem clara quando ainda não há tarefas cadastradas.

### Regras de validação

| Campo | Regra |
|---|---|
| Título | Obrigatório. Vazio ou só com espaços é recusado e o programa pergunta de novo. |
| Prioridade | Só aceita **Alta**, **Média** (ou Media) e **Baixa**. Outra resposta mostra erro e pergunta de novo. |
| Data limite | Formato **DD/MM/AAAA** e precisa ser uma data real (31/02 é recusada). |
| Status | Definido automaticamente como **Pendente**. |

## Tecnologias

- Python 3 (só a biblioteca padrão, nada para instalar)
- Git e GitHub

## Estrutura do repositório

```
tasktracker-projeto/
├── README.md                    # Este arquivo
├── .gitignore                   # Arquivos que o Git deve ignorar
├── docs/
│   └── planejamento_logico.pdf  # Planejamento lógico da Fase 1
└── src/
    └── main.py                  # Código da aplicação
```

## Como instalar e executar

1. Instale o **Python 3.10 ou mais novo** em <https://www.python.org/downloads/>.
   No Windows, marque a opção **"Add Python to PATH"** durante a instalação.
2. Baixe o projeto:
   ```bash
   git clone https://github.com/[SEU-USUARIO]/tasktracker-projeto.git
   cd tasktracker-projeto
   ```
3. Rode o programa:
   ```bash
   python src/main.py
   ```
   No Linux ou Mac pode ser `python3 src/main.py`.

## Exemplo de uso

```
TaskTracker
Gerenciador de tarefas no terminal

1. Cadastrar nova tarefa
2. Visualizar tarefas cadastradas
3. Sair da aplicação
Escolha uma opção: 1

Nova tarefa
Título:
Erro: o título não pode ficar vazio.
Título: Estudar Docker
Descrição (opcional): Volumes e compose
Prioridade (Alta, Média ou Baixa): urgente
Erro: prioridade inválida. Use Alta, Média ou Baixa.
Prioridade (Alta, Média ou Baixa): alta
Data limite (DD/MM/AAAA): 20/10/2026
Tarefa cadastrada com sucesso! Status: Pendente.
```
