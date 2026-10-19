"""TaskTracker: gerenciador de tarefas no terminal.

Como rodar:  python src/main.py
"""

# Lista que guarda as tarefas enquanto o programa está aberto
tarefas = []


# ---------- Funções do menu ----------

def cadastrar_tarefa():
    print("\nNova tarefa")
    tarefa = {
        "titulo": input("Título: ").strip(),
        "descricao": input("Descrição (opcional): ").strip(),
        "prioridade": input("Prioridade (Alta, Média ou Baixa): ").strip(),
        "data_limite": input("Data limite (DD/MM/AAAA): ").strip(),
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
