from crud_usuario import menu_u
from crud_habitos import menu_h
from registros_diarios import menu_rd

def menu():
    while True:
        print("\n=== Bem-vindo ao HabitPlanner ===")
        print("1 - Usuários")
        print("2 - Hábitos")
        print("3 - Registros diários")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_u()
        
        elif opcao == "2":
            menu_h()
        
        elif opcao == "3":
            menu_rd()

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()