# TaskTracker

Gerenciador de tarefas com **menu no terminal** (Python 3) e **painel web** (Flask + JavaScript),
empacotado com Docker. O terminal e o site usam as mesmas regras e o mesmo banco de dados.

Projeto do **Bootcamp II**: Juan Talyson Macêdo Dos Santos, Ciências da computação, polo ASA NORTE.

Vídeo de demonstração: [LINK DO YOUTUBE]

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
  porque ficam na pasta `dados/` do projeto (a mesma usada sem Docker). No modo 2 elas
  somem ao sair; para guardar, use `docker run -it --rm -v "${PWD}/dados:/app/dados" tasktracker`.

### Extra: painel web e API

```bash
docker compose up web
```

Depois abra <http://localhost:8000> no navegador. A documentação da API fica em
<http://localhost:8000/docs>. Para parar, aperte `Ctrl+C`.

O site lê o mesmo banco que o terminal: uma tarefa cadastrada pelo menu aparece no painel, e vice-versa.

## Descrição

Muita gente perde prazos porque anota as tarefas em lugares diferentes, ou nem anota.
O TaskTracker reúne tudo num lugar só: você cadastra a tarefa com título, descrição,
prioridade e data limite, e acompanha os prazos pelo terminal ou pelo navegador.

### Terminal

- Menu contínuo com 3 opções: cadastrar tarefa, visualizar tarefas e sair.
- Listagem em tabela com o prazo de cada tarefa ("vence em 3 dias", "atrasada há 1 dia") e totais por prioridade.
- Mensagem clara quando ainda não há tarefas cadastradas.

### Painel web

- **Visão geral:** total de tarefas, pendentes, concluídas, atrasadas e as que vencem em 7 dias,
  gráfico por prioridade e lista dos próximos prazos.
- **Tarefas:** tabela com busca, filtros por prioridade e status, botão **Concluir** e formulário de cadastro.
- **API:** página com a documentação dos endpoints.

### Regras de validação (iguais no terminal e no site)

| Campo | Regra |
|---|---|
| Título | Obrigatório. Vazio ou só com espaços é recusado. |
| Descrição | Livre e opcional. |
| Prioridade | Só aceita **Alta**, **Média** (ou Media) e **Baixa**, sem diferenciar maiúsculas. |
| Data limite | Formato **DD/MM/AAAA** e precisa ser uma data real (31/02 é recusada). |
| Status | Começa sempre como **Pendente**. Pelo site a tarefa pode virar **Concluída**. |

## API

| Método | Caminho | O que faz |
|---|---|---|
| GET | `/tarefas` | Lista as tarefas (filtros opcionais `?prioridade=` e `?status=`) |
| POST | `/tarefas` | Cadastra uma tarefa (JSON com `titulo`, `descricao`, `prioridade`, `data_limite`) |
| PATCH | `/tarefas/{id}/concluir` | Marca a tarefa como Concluída |
| GET | `/estatisticas` | Totais usados na visão geral |
| GET | `/saude` | Verifica se a API está no ar (healthcheck) |

Erros de validação respondem **422** com a mesma mensagem do terminal:

```json
{ "erro": { "campo": "data_limite", "mensagem": "Erro: data inválida. Use DD/MM/AAAA com uma data real." } }
```

## O Dockerfile, linha por linha

| Linha | O que faz |
|---|---|
| `FROM python:3.11-slim` | Usa uma imagem leve que já tem o Python 3.11. |
| `WORKDIR /app` | Define a pasta de trabalho dentro do container. |
| `ENV PYTHONUNBUFFERED=1` | Faz os `print()` aparecerem na hora. |
| `ENV TZ=America/Sao_Paulo` | Usa o horário de Brasília, para "vence hoje" e "atrasada" baterem com o dia certo. |
| `ENV TASKTRACKER_DB=...` | Diz onde o banco SQLite fica (pasta ligada ao volume). |
| `COPY requirements.txt` + `RUN pip install` | Instala o Flask. |
| `COPY src/ /app/src/` | Copia o código para dentro da imagem. |
| `CMD ["python", "src/main.py"]` | Por padrão, abre o menu do terminal. |

## Arquitetura

```
  Terminal (main.py)          Navegador (app.js)
          │                          │ fetch()
          │                   API Flask (app.py)
          └───────────┬──────────────┘
                      ▼
           Regras (tarefas.py)
                      ▼
           Banco SQLite (banco.py)  →  dados/tasktracker.db
```

## Tecnologias

- **Python 3.11**: terminal, regras e banco (SQLite, que já vem com o Python)
- **Flask 3**: API e páginas do site
- **HTML, CSS e JavaScript puro**: painel web
- **Docker e Docker Compose**: empacotamento e execução
- **unittest**: testes automáticos (já vem com o Python)
- **Git e GitHub**: versionamento

## Estrutura do repositório

```
tasktracker-projeto/
├── .gitignore
├── .dockerignore              # O que não vai para dentro da imagem
├── docs/
│   └── planejamento_logico.pdf  # Planejamento da Fase 1 (rastreabilidade)
├── src/
│   ├── main.py                # Menu do terminal
│   ├── tarefas.py             # Regras e validações (usadas pelo terminal e pelo site)
│   ├── banco.py               # Banco SQLite
│   ├── app.py                 # API e site (Flask)
│   └── web/
│       ├── templates/         # Páginas HTML (painel e documentação da API)
│       └── static/            # app.js e style.css
├── tests/
│   └── test_tarefas.py        # Testes automáticos
├── requirements.txt           # Dependências (Flask)
├── Dockerfile                 # Receita da imagem
├── docker-compose.yml         # Terminal interativo + serviço web
└── README.md
```

## Rodar sem Docker

Com o **Python 3.10 ou mais novo** instalado (no Windows, marque **"Add Python to PATH"**):

```bash
# 1. Criar e ativar um ambiente virtual
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux ou Mac

# 2. Instalar o Flask
pip install -r requirements.txt

# 3. Rodar
python src/main.py              # terminal
python src/app.py               # site em http://localhost:8000
```

O terminal funciona mesmo sem instalar nada (só o site precisa do Flask).
As tarefas ficam no arquivo `dados/tasktracker.db`, o mesmo usado pelo Docker.

## Testes

```bash
python -m unittest discover -s tests -v
```
