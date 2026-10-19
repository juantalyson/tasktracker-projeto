"""TaskTracker: gerenciador de tarefas no terminal.

Como rodar:  python src/main.py
"""

import banco
import tarefas


def perguntar_ate_valido(pergunta, validar):
    """Repete a pergunta até a função de validação aceitar a resposta."""
    while True:
        resposta = input(pergunta)
        try:
            validar(resposta)
            return resposta
        except tarefas.ErroValidacao as erro:
            print(erro.mensagem)


def cadastrar_tarefa():
    print("\nNova tarefa")
    titulo = perguntar_ate_valido("Título: ", tarefas.validar_titulo)
    descricao = input("Descrição (opcional): ")
    prioridade = perguntar_ate_valido("Prioridade (Alta, Média ou Baixa): ", tarefas.validar_prioridade)
    data_limite = perguntar_ate_valido("Data limite (DD/MM/AAAA): ", tarefas.validar_data)

    tarefa = banco.salvar(tarefas.nova_tarefa(titulo, descricao, prioridade, data_limite))
    print(f"Tarefa cadastrada com sucesso! Status: {tarefa['status']}.")


def _cortar(texto, limite):
    """Corta textos longos para a tabela não quebrar."""
    return texto if len(texto) <= limite else texto[: limite - 1] + "…"


def listar_tarefas():
    lista = banco.listar()
    if not lista:
        print("\nNenhuma tarefa cadastrada no momento.")
        return

    cabecalho = ["#", "Título", "Descrição", "Prioridade", "Data limite", "Prazo", "Status"]
    linhas = [
        [
            str(t["id"]),
            _cortar(t["titulo"], 28),
            _cortar(t["descricao"] or "—", 28),
            t["prioridade"],
            tarefas.data_br(t["data_limite"]),
            tarefas.texto_prazo(t),
            t["status"],
        ]
        for t in lista
    ]

    # Largura de cada coluna = maior texto daquela coluna
    larguras = [max(len(linha[i]) for linha in [cabecalho] + linhas) for i in range(len(cabecalho))]

    def formatar(linha):
        return "  ".join(valor.ljust(larguras[i]) for i, valor in enumerate(linha))

    print("\nTarefas cadastradas\n")
    print(formatar(cabecalho))
    print("-" * len(formatar(cabecalho)))
    for linha in linhas:
        print(formatar(linha))

    numeros = tarefas.estatisticas(lista)
    por_prioridade = " | ".join(
        f"{nome}: {dados['total']}" for nome, dados in numeros["por_prioridade"].items()
    )
    print(f"\nTotal: {numeros['total']} | {por_prioridade} | Atrasadas: {numeros['atrasadas']}")


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
