usuario = []


def criar_usuario(nome, email):

  
    for u in usuario:
        if u["nome"] == nome and u["email"] == email:
            print("Usuário já existente!")
            return

    novo = {
        "id": len(usuario) + 1,
        "nome": nome,
        "email": email
    }

    usuario.append(novo)
    print(f"Usuário '{nome}' criado com sucesso!")


def listar_usuario():

    if not usuario:
        print("Nenhum usuário cadastrado.")
    else:
        print("\nLista de usuários:")
        for u in usuario:
            print(f"ID: {u['id']} | Nome: {u['nome']} | Email: {u['email']}")


def atualizar_usuario(id_usuario, nome=None, email=None):

    for u in usuario:
        if u["id"] == id_usuario:

            if nome:
                u["nome"] = nome
            if email:
                u["email"] = email

            print(f"Usuário ID {id_usuario} atualizado com sucesso!")
            return

    print("Usuário não encontrado.")


def deletar_usuario(id_usuario):

    global usuario
    novo = [u for u in usuario if u["id"] != id_usuario]

    if len(novo) == len(usuario):
        print("Usuário não encontrado.")
    else:
        usuario = novo
        print(f"Usuário ID {id_usuario} removido com sucesso!")


def menu():
    while True:
        print("\n=== MENU DE USUÁRIO ===")
        print("1 - Criar usuário")
        print("2 - Listar usuários")
        print("3 - Atualizar usuário")
        print("4 - Deletar usuário")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("Informe o nome do seu usuário! \n")
            nome = input("Nome: ")
            email = input("Email: ")
            criar_usuario(nome, email)

        elif opcao == "2":
            listar_usuario()

        elif opcao == "3":
            id_usuario = int(input("ID do usuário: "))
            nome = input("Novo nome do usuário: ") or None
            email = input("Novo email do usuário:  ") or None
            atualizar_usuario(id_usuario, nome, email)

        elif opcao == "4":
            id_usuario = int(input("ID do usuário: "))
            deletar_usuario(id_usuario)

        elif opcao == "5":
            print("Saindo...")
            break

        else:
            print("Opção inválida!")


if __name__ == "__main__":
    menu()