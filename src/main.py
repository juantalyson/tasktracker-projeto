"""TaskTracker: gerenciador de tarefas no terminal.

Como rodar:  python src/main.py
"""

import unicodedata
from datetime import datetime

# Lista que guarda as tarefas enquanto o programa está aberto
tarefas = []

PRIORIDADES = ["Alta", "Média", "Baixa"]


# ---------- Validações ----------

def sem_acento(texto):
    """'Média' -> 'media'. Usado para comparar a prioridade digitada."""
    normalizado = unicodedata.normalize("NFD", texto)
    return "".join(c for c in normalizado if unicodedata.category(c) != "Mn").lower()


def ler_titulo():
    """Título obrigatório: repete a pergunta enquanto vier vazio ou só com espaços."""
    while True:
        titulo = input("Título: ").strip()
        if titulo:
            return titulo
        print("Erro: o título não pode ficar vazio.")


def ler_prioridade():
    """Aceita só Alta, Média (ou Media) e Baixa. Qualquer outra coisa: erro e pergunta de novo."""
    while True:
        digitado = sem_acento(input("Prioridade (Alta, Média ou Baixa): ").strip())
        for prioridade in PRIORIDADES:
            if digitado == sem_acento(prioridade):
                return prioridade
        print("Erro: prioridade inválida. Use Alta, Média ou Baixa.")


def ler_data_limite():
    """Data no formato DD/MM/AAAA e que exista de verdade (31/02 é recusada)."""
    while True:
        texto = input("Data limite (DD/MM/AAAA): ").strip()
        try:
            datetime.strptime(texto, "%d/%m/%Y")
            return texto
        except ValueError:
            print("Erro: data inválida. Use DD/MM/AAAA com uma data real.")


# ---------- Funções do menu ----------

def cadastrar_tarefa():
    print("\nNova tarefa")
    tarefa = {
        "titulo": ler_titulo(),
        "descricao": input("Descrição (opcional): ").strip(),
        "prioridade": ler_prioridade(),
        "data_limite": ler_data_limite(),
        "status": "Pendente",  # toda tarefa nova começa pendente
    }
    tarefas.append(tarefa)
    print("Tarefa cadastrada com sucesso! Status: Pendente.")


def listar_tarefas():
    if not tarefas:
        print("\nNenhuma tarefa cadastrada no momento.")
        return

    print("\nTarefas cadastradas")
    for numero, tarefa in enumerate(tarefas, start=1):
        print(f"\nTarefa {numero}")
        print(f"  Título:      {tarefa['titulo']}")
        print(f"  Descrição:   {tarefa['descricao'] or '—'}")
        print(f"  Prioridade:  {tarefa['prioridade']}")
        print(f"  Data limite: {tarefa['data_limite']}")
        print(f"  Status:      {tarefa['status']}")
    print(f"\nTotal: {len(tarefas)} tarefa(s)")


def mostrar_menu():
    print("\n1. Cadastrar nova tarefa")
    print("2. Visualizar tarefas cadastradas")
    print("3. Sair da aplicação")


def main():
    print("TaskTracker")
    print("Gerenciador de tarefas no terminal")
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            cadastrar_tarefa()
        elif opcao == "2":
            listar_tarefas()
        elif opcao == "3":
            print("Até logo!")
            break
        else:
            print("Opção inválida. Digite 1, 2 ou 3.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C ou fim da entrada: sai sem mostrar erro
        print("\nAté logo!")
