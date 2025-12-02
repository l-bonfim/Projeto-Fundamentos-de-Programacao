import json
import os

ARQUIVO_HABITOS = 'habitos.json'
ARQUIVO_USUARIOS = 'usuarios.json'

def carregar_usuarios():
    """Carrega usuários do arquivo JSON"""
    if not os.path.exists(ARQUIVO_USUARIOS):
        return []
    try:
        with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def carregar_habitos():
    """Carrega hábitos do arquivo JSON"""
    if not os.path.exists(ARQUIVO_HABITOS):
        return []
    with open(ARQUIVO_HABITOS, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_habitos(habitos):
    """Salva hábitos no arquivo JSON"""
    with open(ARQUIVO_HABITOS, 'w', encoding='utf-8') as f:
        json.dump(habitos, f, indent=4, ensure_ascii=False)

def listar_usuarios_com_ids():
    """Lista usuários disponíveis com seus IDs"""
    usuarios = carregar_usuarios()
    if not usuarios:
        print("Nenhum usuário cadastrado. Cadastre um usuário primeiro!")
        return None
    
    print("\n=== USUÁRIOS DISPONÍVEIS ===")
    for usuario in usuarios:
        print(f"ID: {usuario['id']} | Nome: {usuario['nome']} | Email: {usuario['email']}")
    print()
    return usuarios

def criar_habito():
    """Cria um novo hábito vinculado a um usuário"""
    usuarios = listar_usuarios_com_ids()
    if not usuarios:
        return
    
    habitos = carregar_habitos()
    
    try:
        usuario_id = int(input("Digite o ID do usuário para vincular o hábito: "))
    except ValueError:
        print("ID inválido! Digite um número.")
        return
    
    usuario_existe = any(usuario['id'] == usuario_id for usuario in usuarios)
    if not usuario_existe:
        print(f"Usuário com ID {usuario_id} não encontrado!")
        return
    
    if habitos:
        id_novo = max([h['id'] for h in habitos]) + 1
    else:
        id_novo = 1

    print("\n=== CADASTRO DE HÁBITO ===")
    nome = input("Nome do hábito: ").strip()
    if not nome:
        print("Nome do hábito é obrigatório!")
        return
    
    categoria = input("Categoria (ex: saúde, produtividade, etc): ").strip()
    frequencia = input("Frequência (diário, semanal, etc): ").strip()
    meta = input("Meta associada (ex: 2L, 30min, 8h): ").strip()

    habito = {
        "id": id_novo,
        "usuario_id": usuario_id, 
        "nome": nome,
        "categoria": categoria,
        "frequencia": frequencia,
        "meta": meta
    }

    habitos.append(habito)
    salvar_habitos(habitos)
    print(f"\n✅ Hábito '{nome}' cadastrado com sucesso para o usuário ID {usuario_id}!\n")

def listar_habitos():
    """Lista hábitos mostrando também o usuário dono"""
    habitos = carregar_habitos()
    usuarios = carregar_usuarios()
    
    if not habitos:
        print("Nenhum hábito cadastrado.")
        return
    
    usuarios_dict = {usuario['id']: usuario for usuario in usuarios}
    
    print("\n=== LISTA DE HÁBITOS ===")
    for habito in habitos:
        usuario_id = habito.get('usuario_id')
        usuario_info = usuarios_dict.get(usuario_id, {})
        nome_usuario = usuario_info.get('nome', 'Usuário não encontrado')
        
        print(f"[ID: {habito['id']}] Usuário: {nome_usuario} (ID: {usuario_id})")
        print(f"   Hábito: {habito['nome']}")
        print(f"   Categoria: {habito['categoria']} | Frequência: {habito['frequencia']}")
        print(f"   Meta: {habito['meta']}")
        print("-" * 40)

def atualizar_habito():
    """Atualiza um hábito existente"""
    habitos = carregar_habitos()
    if not habitos:
        print("Nenhum hábito cadastrado.")
        return
    
    listar_habitos()
    
    try:
        id_editar = int(input("\nDigite o ID do hábito que deseja atualizar: "))
    except ValueError:
        print("ID inválido! Digite um número.")
        return
    
    habito_encontrado = None
    for habito in habitos:
        if habito['id'] == id_editar:
            habito_encontrado = habito
            break
    
    if not habito_encontrado:
        print("Hábito não encontrado.")
        return
    
    print(f"\nHábito atual: {habito_encontrado['nome']}")
    print(f"Usuário atual: ID {habito_encontrado.get('usuario_id', 'Não vinculado')}")
    
    alterar_usuario = input("Deseja alterar o usuário vinculado? (s/n): ").lower()
    
    if alterar_usuario == 's':
        usuarios = listar_usuarios_com_ids()
        if usuarios:
            try:
                novo_usuario_id = int(input("Digite o novo ID do usuário: "))
                usuario_existe = any(usuario['id'] == novo_usuario_id for usuario in usuarios)
                if usuario_existe:
                    habito_encontrado['usuario_id'] = novo_usuario_id
                    print("Usuário alterado com sucesso!")
                else:
                    print(f"Usuário com ID {novo_usuario_id} não encontrado!")
                    return
            except ValueError:
                print("ID inválido!")
                return
    
    print("\nDeixe em branco para manter o valor atual.")
    
    novo_nome = input(f"Nome atual [{habito_encontrado['nome']}]: ").strip()
    if novo_nome:
        habito_encontrado['nome'] = novo_nome
    
    nova_categoria = input(f"Categoria atual [{habito_encontrado['categoria']}]: ").strip()
    if nova_categoria:
        habito_encontrado['categoria'] = nova_categoria
    
    nova_frequencia = input(f"Frequência atual [{habito_encontrado['frequencia']}]: ").strip()
    if nova_frequencia:
        habito_encontrado['frequencia'] = nova_frequencia
    
    nova_meta = input(f"Meta atual [{habito_encontrado['meta']}]: ").strip()
    if nova_meta:
        habito_encontrado['meta'] = nova_meta
    
    salvar_habitos(habitos)
    print("\n✅ Hábito atualizado com sucesso!\n")

def excluir_habito():
    """Exclui um hábito"""
    habitos = carregar_habitos()
    if not habitos:
        print("Nenhum hábito cadastrado.")
        return
    
    listar_habitos()
    
    try:
        id_excluir = int(input("\nDigite o ID do hábito que deseja excluir: "))
    except ValueError:
        print("ID inválido! Digite um número.")
        return
    
    habitos_antes = len(habitos)
    novos_habitos = [h for h in habitos if h['id'] != id_excluir]
    
    if len(novos_habitos) != habitos_antes:
        salvar_habitos(novos_habitos)
        print("\n✅ Hábito excluído com sucesso!\n")
    else:
        print("ID não encontrado.")

def listar_habitos_por_usuario():
    """Lista hábitos de um usuário específico"""
    usuarios = listar_usuarios_com_ids()
    if not usuarios:
        return
    
    try:
        usuario_id = int(input("Digite o ID do usuário para listar seus hábitos: "))
    except ValueError:
        print("ID inválido! Digite um número.")
        return
    
    usuario_existe = any(usuario['id'] == usuario_id for usuario in usuarios)
    if not usuario_existe:
        print(f"Usuário com ID {usuario_id} não encontrado!")
        return
    
    habitos = carregar_habitos()
    habitos_usuario = [h for h in habitos if h.get('usuario_id') == usuario_id]
    
    nome_usuario = next((u['nome'] for u in usuarios if u['id'] == usuario_id), "Usuário Desconhecido")
    
    if not habitos_usuario:
        print(f"\nO usuário '{nome_usuario}' não possui hábitos cadastrados.")
        return
    
    print(f"\n=== HÁBITOS DE {nome_usuario.upper()} (ID: {usuario_id}) ===")
    for habito in habitos_usuario:
        print(f"[{habito['id']}] {habito['nome']}")
        print(f"   Categoria: {habito['categoria']}")
        print(f"   Frequência: {habito['frequencia']}")
        print(f"   Meta: {habito['meta']}")
        print("-" * 30)

def menu():
    """Menu principal do sistema de hábitos"""
    while True:
        print("""
=== SISTEMA DE HÁBITOS SAUDÁVEIS ===
1. Cadastrar hábito (vinculado a um usuário)
2. Listar todos os hábitos
3. Listar hábitos por usuário
4. Atualizar hábito
5. Excluir hábito
0. Sair
""")
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            criar_habito()
        elif opcao == "2":
            listar_habitos()
        elif opcao == "3":
            listar_habitos_por_usuario()
        elif opcao == "4":
            atualizar_habito()
        elif opcao == "5":
            excluir_habito()
        elif opcao == "0":
            print("Encerrando sistema de hábitos...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()