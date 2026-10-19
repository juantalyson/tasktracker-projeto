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
- `--rm` apaga o container quando você sai do programa.

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

## O Dockerfile, linha por linha

| Linha | O que faz |
|---|---|
| `FROM python:3.11-slim` | Usa uma imagem leve que já tem o Python 3.11. |
| `WORKDIR /app` | Define a pasta de trabalho dentro do container. |
| `ENV PYTHONUNBUFFERED=1` | Faz os `print()` aparecerem na hora. |
| `COPY src/ /app/src/` | Copia o código para dentro da imagem. |
| `CMD ["python", "src/main.py"]` | Comando que roda quando o container inicia. |

## Tecnologias

- Python 3.11 (só a biblioteca padrão)
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
│   └── main.py                # Código Python da Fase 2
├── Dockerfile                 # Receita da imagem (Fase 3)
├── docker-compose.yml         # Execução interativa orquestrada (Fase 3)
└── README.md
```

## Rodar sem Docker

Com o Python 3.10 ou mais novo instalado:

```bash
python src/main.py
```
