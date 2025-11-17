import json
import os

ARQUIVO = 'habitos.json'

def carregar_habitos():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_habitos(habitos):
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(habitos, f, indent=4, ensure_ascii=False)

def criar_habito():
    habitos = carregar_habitos()
    id_novo = max([h['id'] for h in habitos], default=0) + 1

    nome = input("Nome do hábito: ")
    categoria = input("Categoria (ex: saúde, produtividade, etc): ")
    frequencia = input("Frequência (diário, semanal, etc): ")
    meta = input("Meta associada (ex: 2L, 30min, 8h): ")

    habito = {
        "id": id_novo,
        "nome": nome,
        "categoria": categoria,
        "frequencia": frequencia,
        "meta": meta
    }

    habitos.append(habito)
    salvar_habitos(habitos)
    print("\n Hábito cadastrado com sucesso!\n")

def listar_habitos():
    habitos = carregar_habitos()
    if not habitos:
        print("Nenhum hábito cadastrado.")
        return
    for h in habitos:
        print(f"[{h['id']}] {h['nome']} - {h['categoria']} ({h['frequencia']}) Meta: {h['meta']}")

def atualizar_habito():
    habitos = carregar_habitos()
    listar_habitos()
    id_editar = int(input("\nDigite o ID do hábito que deseja atualizar: "))
    for h in habitos:
        if h['id'] == id_editar:
            h['nome'] = input("Novo nome do seu hábito: ")
            h['categoria'] = input("Nova categoria (ex: saúde, produtividade, etc): ") 
            h['frequencia'] = input("Nova frequência (diário, semanal, etc): ") 
            h['meta'] = input("Nova meta (ex: 2L, 30min, 8h): ")
            salvar_habitos(habitos)
            print("\n Hábito atualizado com sucesso!\n")
            return
    print("Hábito não encontrado.")

def excluir_habito():
    habitos = carregar_habitos()
    listar_habitos()
    id_excluir = int(input("\nDigite o ID do hábito que deseja excluir: "))
    novos = [h for h in habitos if h['id'] != id_excluir]
    if len(novos) != len(habitos):
        salvar_habitos(novos)
        print("\n Hábito excluído com sucesso!\n")
    else:
        print("ID não encontrado.")

def menu():
    while True:
        print("""
=== SISTEMA DE HÁBITOS SAUDÁVEIS ===
1. Cadastrar hábito
2. Listar hábitos
3. Atualizar hábito
4. Excluir hábito
0. Sair
""")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            criar_habito()
        elif opcao == "2":
            listar_habitos()
        elif opcao == "3":
            atualizar_habito()
        elif opcao == "4":
            excluir_habito()
        elif opcao == "0":
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida!")

menu()
