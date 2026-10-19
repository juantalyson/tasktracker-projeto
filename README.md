# TaskTracker

Gerenciador de tarefas no terminal, feito em Python 3 e empacotado com Docker.

Projeto do **Bootcamp II**: [SEU NOME COMPLETO], [SEU CURSO], polo [ASA NORTE ou TAGUATINGA].

## Como rodar com Docker

Pré-requisito: **Docker Desktop** instalado e aberto (<https://www.docker.com/products/docker-desktop/>).
Rode os comandos na pasta do projeto, onde estão o `Dockerfile` e o `docker-compose.yml`.

### 1. Construir a imagem

```bash
docker build -t tasktracker .
```

### 2. Rodar o container em modo isolado

```bash
docker run -it --rm tasktracker
```

### 3. Rodar via orquestração (recomendado)

```bash
docker compose run --rm tasktracker-app
```

- `-it` (no `docker run`) e `stdin_open: true` + `tty: true` (no `docker-compose.yml`)
  deixam o terminal interativo, para o `input()` do Python receber o que você digita.
- `--rm` apaga o container quando você sai. As tarefas **não** se perdem no modo 3,
  porque ficam no volume `tasktracker-data`. No modo 2 elas somem ao sair; para guardar,
  use `docker run -it --rm -v tasktracker-data:/app/dados tasktracker`.

## Descrição

Muita gente perde prazos porque anota as tarefas em lugares diferentes, ou nem anota.
O TaskTracker reúne tudo num lugar só: você cadastra a tarefa com título, descrição,
prioridade e data limite, e depois vê a lista completa no terminal.

### Funcionalidades

- Menu contínuo com 3 opções: cadastrar tarefa, visualizar tarefas e sair.
- Cada tarefa tem **título**, **descrição**, **prioridade**, **data limite** e **status**.
- O status começa sempre como **Pendente**.
- Listagem em tabela com o prazo de cada tarefa ("vence em 3 dias", "atrasada há 1 dia") e totais por prioridade.
- As tarefas ficam salvas num banco **SQLite** (arquivo único, já vem com o Python).
- Mensagem clara quando ainda não há tarefas cadastradas.

### Regras de validação

| Campo | Regra |
|---|---|
| Título | Obrigatório. Vazio ou só com espaços é recusado e o programa pergunta de novo. |
| Prioridade | Só aceita **Alta**, **Média** (ou Media) e **Baixa**. Outra resposta mostra erro e pergunta de novo. |
| Data limite | Formato **DD/MM/AAAA** e precisa ser uma data real (31/02 é recusada). |
| Status | Definido automaticamente como **Pendente**. |

## O Dockerfile, linha por linha

| Linha | O que faz |
|---|---|
| `FROM python:3.11-slim` | Usa uma imagem leve que já tem o Python 3.11. |
| `WORKDIR /app` | Define a pasta de trabalho dentro do container. |
| `ENV PYTHONUNBUFFERED=1` | Faz os `print()` aparecerem na hora. |
| `ENV TASKTRACKER_DB=...` | Diz onde o banco SQLite fica (pasta ligada ao volume). |
| `COPY src/ /app/src/` | Copia o código para dentro da imagem. |
| `CMD ["python", "src/main.py"]` | Comando que roda quando o container inicia. |

## Tecnologias

- Python 3.11 (só a biblioteca padrão, com SQLite e unittest)
- Docker e Docker Compose
- Git e GitHub

## Estrutura do repositório

```
tasktracker-projeto/
├── .gitignore
├── .dockerignore              # O que não vai para dentro da imagem
├── docs/
│   └── planejamento_logico.pdf  # Planejamento da Fase 1 (rastreabilidade)
├── src/
│   ├── main.py                # Menu do terminal
│   ├── tarefas.py             # Regras e validações
│   └── banco.py               # Banco SQLite
├── tests/
│   └── test_tarefas.py        # Testes automáticos
├── Dockerfile                 # Receita da imagem (Fase 3)
├── docker-compose.yml         # Execução interativa orquestrada (Fase 3)
└── README.md
```

## Rodar sem Docker

Com o Python 3.10 ou mais novo instalado:

```bash
python src/main.py
```

Sem Docker, as tarefas ficam no arquivo `dados/tasktracker.db`.

## Testes

```bash
python -m unittest discover -s tests -v
```
