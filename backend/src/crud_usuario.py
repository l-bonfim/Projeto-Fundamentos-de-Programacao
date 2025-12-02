import json
import os

JSON_FILE = "usuarios.json"

def carregar_usuarios():
    """Carrega usuários do arquivo JSON"""
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def salvar_usuarios(usuarios):
    """Salva a lista de usuários no arquivo JSON"""
    try:
        with open(JSON_FILE, 'w', encoding='utf-8') as file:
            json.dump(usuarios, file, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Erro ao salvar usuários: {e}")
        return False

def criar_usuario(nome, email):
    """Cria um novo usuário"""
    usuarios = carregar_usuarios()
    
    # Verificar se usuário já existe
    for u in usuarios:
        if u["email"] == email:
            print("Usuário com este email já existe!")
            return False
    
    # Determinar próximo ID
    if usuarios:
        proximo_id = max(u["id"] for u in usuarios) + 1
    else:
        proximo_id = 1
    
    novo_usuario = {
        "id": proximo_id,
        "nome": nome,
        "email": email
    }
    
    usuarios.append(novo_usuario)
    
    if salvar_usuarios(usuarios):
        print(f"Usuário '{nome}' criado com sucesso!")
        return True
    else:
        print("Erro ao salvar usuário!")
        return False

def listar_usuarios():
    """Lista todos os usuários"""
    usuarios = carregar_usuarios()
    
    if not usuarios:
        print("Nenhum usuário cadastrado.")
    else:
        print("\nLista de usuários:")
        for u in usuarios:
            print(f"ID: {u['id']} | Nome: {u['nome']} | Email: {u['email']}")

def atualizar_usuario(id_usuario, nome=None, email=None):
    """Atualiza um usuário existente"""
    usuarios = carregar_usuarios()
    usuario_encontrado = False
    
    for u in usuarios:
        if u["id"] == id_usuario:
            usuario_encontrado = True
            
            # Verificar se o novo email já existe em outro usuário
            if email:
                for outro_usuario in usuarios:
                    if outro_usuario["id"] != id_usuario and outro_usuario["email"] == email:
                        print("Email já está em uso por outro usuário!")
                        return False
            
            # Atualizar dados
            if nome:
                u["nome"] = nome
            if email:
                u["email"] = email
            
            break
    
    if not usuario_encontrado:
        print("Usuário não encontrado.")
        return False
    
    if salvar_usuarios(usuarios):
        print(f"Usuário ID {id_usuario} atualizado com sucesso!")
        return True
    else:
        print("Erro ao salvar alterações!")
        return False

def deletar_usuario(id_usuario):
    """Remove um usuário"""
    usuarios = carregar_usuarios()
    usuarios_antes = len(usuarios)
    
    usuarios = [u for u in usuarios if u["id"] != id_usuario]
    usuarios_depois = len(usuarios)
    
    if usuarios_antes == usuarios_depois:
        print("Usuário não encontrado.")
        return False
    
    if salvar_usuarios(usuarios):
        print(f"Usuário ID {id_usuario} removido com sucesso!")
        return True
    else:
        print("Erro ao salvar alterações!")
        return False

def menu():
    """Menu principal do sistema"""
    while True:
        print("\n=== MENU DE USUÁRIO ===")
        print("1 - Criar usuário")
        print("2 - Listar usuários")
        print("3 - Atualizar usuário")
        print("4 - Deletar usuário")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("Informe os dados do usuário:")
            nome = input("Nome: ").strip()
            email = input("Email: ").strip()
            
            if nome and email:
                criar_usuario(nome, email)
            else:
                print("Nome e email são obrigatórios!")

        elif opcao == "2":
            listar_usuarios()

        elif opcao == "3":
            try:
                id_usuario = int(input("ID do usuário: "))
                nome = input("Novo nome (deixe em branco para não alterar): ").strip() or None
                email = input("Novo email (deixe em branco para não alterar): ").strip() or None
                
                if nome is None and email is None:
                    print("Nenhuma alteração fornecida.")
                else:
                    atualizar_usuario(id_usuario, nome, email)
            except ValueError:
                print("ID deve ser um número!")

        elif opcao == "4":
            try:
                id_usuario = int(input("ID do usuário: "))
                deletar_usuario(id_usuario)
            except ValueError:
                print("ID deve ser um número!")

        elif opcao == "5":
            print("Saindo...")
            break

        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()