import json
import os
from datetime import datetime

ARQUIVO_REGISTROS = "registros_diarios.json"
ARQUIVO_HABITOS = "habitos.json"
ARQUIVO_USUARIOS = "usuarios.json"

def carregar_json(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def salvar_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Erro ao salvar {path}: {e}")
        return False

def carregar_usuarios():
    return carregar_json(ARQUIVO_USUARIOS)


def carregar_habitos():
    return carregar_json(ARQUIVO_HABITOS)


def carregar_registros():
    return carregar_json(ARQUIVO_REGISTROS)


def salvar_registros(registros):
    return salvar_json(ARQUIVO_REGISTROS, registros)


def listar_usuarios_console():
    usuarios = carregar_usuarios()
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return []
    print("\n=== USUÁRIOS ===")
    for u in usuarios:
        print(f"ID: {u['id']} | Nome: {u.get('nome','-')} | Email: {u.get('email','-')}")
    print()
    return usuarios


def listar_habitos_console():
    habitos = carregar_habitos()
    usuarios = carregar_usuarios()
    usuarios_dict = {u['id']: u for u in usuarios}
    if not habitos:
        print("Nenhum hábito cadastrado.")
        return []
    print("\n=== HÁBITOS ===")
    for h in habitos:
        dono = usuarios_dict.get(h.get('usuario_id'), {})
        nome_dono = dono.get('nome', 'Usuário não encontrado')
        print(f"ID: {h['id']} | Hábito: {h.get('nome','-')} | Usuário: {nome_dono} (ID: {h.get('usuario_id')}) | Categoria: {h.get('categoria','-')} | Frequência: {h.get('frequencia','-')}")
    print()
    return habitos


def buscar_habito_por_id(habitos, habito_id):
    for h in habitos:
        if h['id'] == habito_id:
            return h
    return None


def buscar_usuario_por_id(usuarios, usuario_id):
    for u in usuarios:
        if u['id'] == usuario_id:
            return u
    return None


def gerar_id_unico():
    registros = carregar_registros()
    if registros == []:
        return 1
    else:
        for i in range(len(registros)):
            print(registros[i]["id"] != i+1, registros[i]["id"])
            if registros[i]["id"] != i+1:
                return i+1
        return len(registros)+1
        


def validar_data_input(data_str):

    if not data_str or not data_str.strip():
        return datetime.now().strftime("%d-%m-%Y")
    data_str = data_str.strip()
    for fmt in ("%d-%m-%Y", "%Y-%m-%d"):
        try:
            d = datetime.strptime(data_str, fmt)
            return d.strftime("%d-%m-%Y")
        except ValueError:
            continue
    print("Formato de data não reconhecido. Use DD-MM-AAAA ou AAAA-MM-DD. Usando valor informado.")
    return data_str


def criar_registro():
    habitos = carregar_habitos()
    usuarios = carregar_usuarios()
    if not habitos:
        print("Não há hábitos cadastrados. Cadastre um hábito antes de criar registros.")
        return

    listar_habitos_console()
    try:
        habito_id = int(input("Digite o ID do hábito para vincular o registro: ").strip())
    except ValueError:
        print("ID inválido! Digite um número.")
        return

    habito = buscar_habito_por_id(habitos, habito_id)
    if not habito:
        print(f"Hábito com ID {habito_id} não encontrado.")
        return

    usuario_id = habito.get('usuario_id')
    usuario = buscar_usuario_por_id(usuarios, usuario_id)
    nome_usuario = usuario.get('nome') if usuario else "Usuário não encontrado"

    print(f"\nCriando registro para o hábito '{habito.get('nome')}' (Usuário: {nome_usuario})")
    data_in = input("Data (DD-MM-AAAA) [enter = hoje]: ")
    data = validar_data_input(data_in)

    cumprido = input("Cumprido? (Sim/Nao) [padrão: Sim]: ").strip()
    if not cumprido:
        cumprido = "Sim"
    humor = input("Humor (ex: Feliz/Neutro/Triste) [opcional]: ").strip() or ""
    observacoes = input("Observações [opcional]: ").strip() or ""

    registro = {
        "id": gerar_id_unico(),
        "data": data,
        "habito_id": habito_id,
        "habito_nome": habito.get('nome'),
        "usuario_id": usuario_id,
        "cumprido": cumprido,
        "humor": humor,
        "observacoes": observacoes
    }

    registros = carregar_registros()
    registros.append(registro)
    registros.sort(key = lambda registros: registros["id"])
    if salvar_registros(registros):
        print("Registro criado com sucesso!")
    else:
        print("Erro ao salvar registro.")

def listar_todos_registros():
    registros = carregar_registros()
    if not registros:
        print("Nenhum registro encontrado.")
        return
    usuarios = carregar_usuarios()
    usuarios_dict = {u['id']: u for u in usuarios}
    print("\n=== TODOS OS REGISTROS ===")
    for r in registros:
        usuario = usuarios_dict.get(r.get('usuario_id'), {})
        nome_usuario = usuario.get('nome', 'Usuário não encontrado')
        print(f"[ID: {r['id']}] Data: {r['data']} | Usuário: {nome_usuario} (ID: {r.get('usuario_id')})")
        print(f"   Hábito: {r.get('habito_nome')} (ID: {r.get('habito_id')}) | Cumprido: {r.get('cumprido')}")
        print(f"   Humor: {r.get('humor')} | Obs: {r.get('observacoes')}")
        print("-" * 50)


def listar_registros_por_usuario():
    usuarios = listar_usuarios_console()
    if not usuarios:
        return
    try:
        usuario_id = int(input("Digite o ID do usuário para ver seus registros: ").strip())
    except ValueError:
        print("ID inválido!")
        return
    registros = carregar_registros()
    filtrados = [r for r in registros if r.get('usuario_id') == usuario_id]
    if not filtrados:
        print("Nenhum registro encontrado para esse usuário.")
        return
    print(f"\n=== REGISTROS DO USUÁRIO ID {usuario_id} ===")
    for r in filtrados:
        print(f"[ID: {r['id']}] Data: {r['data']} | Hábito: {r.get('habito_nome')} (ID: {r.get('habito_id')}) | Cumprido: {r.get('cumprido')}")
        print(f"   Humor: {r.get('humor')} | Obs: {r.get('observacoes')}")
        print("-" * 40)


def listar_registros_por_habito():
    habitos = listar_habitos_console()
    if not habitos:
        return
    try:
        habito_id = int(input("Digite o ID do hábito para ver seus registros: ").strip())
    except ValueError:
        print("ID inválido!")
        return
    registros = carregar_registros()
    filtrados = [r for r in registros if r.get('habito_id') == habito_id]
    if not filtrados:
        print("Nenhum registro encontrado para esse hábito.")
        return
    print(f"\n=== REGISTROS DO HÁBITO ID {habito_id} ===")
    for r in filtrados:
        print(f"[ID: {r['id']}] Data: {r['data']} | Cumprido: {r.get('cumprido')} | Humor: {r.get('humor')}")
        print(f"   Obs: {r.get('observacoes')}")
        print("-" * 30)


def atualizar_registro():
    listar_todos_registros()
    registros = carregar_registros()
    if not registros:
        return
    try:
        id_editar = int(input("Digite o ID do registro que deseja atualizar: ").strip())
    except ValueError:
        print("ID inválido!")
        return
    registro = next((r for r in registros if r['id'] == id_editar), None)
    if not registro:
        print("Registro não encontrado.")
        return

    print("\nDeixe em branco para manter o valor atual.")
    novo_data = input(f"Data atual [{registro['data']}]: ").strip()
    if novo_data:
        registro['data'] = validar_data_input(novo_data)

    trocar_habito = input("Deseja alterar o hábito vinculado? (s/n): ").strip().lower()
    if trocar_habito == 's':
        habitos = carregar_habitos()
        listar_habitos_console()
        try:
            novo_habito_id = int(input("Digite o novo ID do hábito: ").strip())
        except ValueError:
            print("ID inválido!")
            return
        novo_habito = buscar_habito_por_id(habitos, novo_habito_id)
        if not novo_habito:
            print("Hábito não encontrado.")
            return
        registro['habito_id'] = novo_habito_id
        registro['habito_nome'] = novo_habito.get('nome')
        registro['usuario_id'] = novo_habito.get('usuario_id')

    novo_cumprido = input(f"Cumprido atual [{registro.get('cumprido')}]: ").strip()
    if novo_cumprido:
        registro['cumprido'] = novo_cumprido
    novo_humor = input(f"Humor atual [{registro.get('humor','')}]: ").strip()
    if novo_humor:
        registro['humor'] = novo_humor
    nova_obs = input(f"Observações atuais [{registro.get('observacoes','')}]: ").strip()
    if nova_obs:
        registro['observacoes'] = nova_obs

    if salvar_registros(registros):
        print("Registro atualizado com sucesso!")
    else:
        print("Erro ao salvar alterações.")


def deletar_registro():
    listar_todos_registros()
    registros = carregar_registros()
    if not registros:
        return
    try:
        id_del = int(input("Digite o ID do registro que deseja deletar: ").strip())
    except ValueError:
        print("ID inválido!")
        return
    novos = [r for r in registros if r['id'] != id_del]
    if len(novos) == len(registros):
        print("Registro não encontrado.")
        return
    if salvar_registros(novos):
        print("Registro deletado com sucesso!")
    else:
        print("Erro ao salvar alterações.")


def menu_rd():
    while True:
        print("""
=== SISTEMA DE REGISTROS DIÁRIOS (VINCULADOS A HÁBITOS) ===
1. Criar registro (vinculado a um hábito)
2. Listar todos os registros
3. Listar registros por usuário
4. Listar registros por hábito
5. Atualizar registro
6. Deletar registro
0. Sair
""")
        opc = input("Escolha uma opção: ").strip()
        if opc == "1":
            criar_registro()
        elif opc == "2":
            listar_todos_registros()
        elif opc == "3":
            listar_registros_por_usuario()
        elif opc == "4":
            listar_registros_por_habito()
        elif opc == "5":
            atualizar_registro()
        elif opc == "6":
            deletar_registro()
        elif opc == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu_rd()
