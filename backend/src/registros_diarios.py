import json
import os
from datetime import datetime



# Caminho do arquivo JSON onde os dados serão salvos

ARQUIVO_JSON = os.path.join("registros_diarios.json")

# ----------- Função auxiliar -----------
def carregando_registros():
# Carrega os registros do arquivo JSON.
    if not os.path.exists(ARQUIVO_JSON):
        return []
    with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
        try:
            return json.load(arquivo)
        except json.JSONDecodeError:
            return []

def salvando_registros(registros):
# Salva a lista de registros no arquivo JSON.
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(registros, arquivo, ensure_ascii=False, indent=4)


def criando_registros(data, habito, cumprido, humor, observacoes):
# Cria um novo registro diário.
    registros = carregando_registros()
    novo_registro = {
        "id": int(datetime.now().timestamp()),
        "data": data,
        "habito": habito,
        "cumprido": cumprido,
        "humor": humor,
        "observacoes": observacoes
    }
    registros.append(novo_registro)
    salvando_registros(registros)
    print("Registro criado com sucesso!")


def listando_registros():
# Exibe todos os registros cadastrados.
    registros = carregando_registros()
    if not registros:
        print("Nenhum registro encontrado.")
        return
    print("\nLISTA DE REGISTROS: ")
    for r in registros:
        print(f"ID: {r['id']} | Data: {r['data']} | Hábito: {r['habito']} | "
              f"Cumprido: {r['cumprido']} | Humor: {r['humor']} | Obs.: {r['observacoes']}")
        

def atualizando_registro(id_registro, novos_dados):
# Atualiza um registro pelo ID.
    registros = carregando_registros()
    for r in registros:
        if r["id"] == id_registro:
            r.update(novos_dados)
            salvando_registros(registros)
            print("Registro atualizado com sucesso!")
            return
    print("Registro não encontrado.")


    
   
def deletando_registro(id_registro):
# Remove um registro pelo ID.
    registros = carregando_registros()
    novos = [r for r in registros if r["id"] != id_registro]
    if len(novos) == len(registros):
        print("Registro não encontrado!")
        return
    salvando_registros(novos)
    print("Registro deletado com sucesso!")

if __name__ == "__main__":
    while True:
        print("\n=== SISTEMA DE REGISTROS DIÁRIOS ===")
        print("1. Criar Registro")
        print("2. Listar Registros")
        print("3. Atualizar Registro")
        print("4. Deletar Registro")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            data = input("Data (DD-MM-AAA): ")
            habito = input("Hábito: ")
            cumprido = bool(input("Cumprido?(True/False): ").capitalize())
            humor = input("Humor(Feliz/Neutro/Triste): ")
            obs = input("Observações: ")
            criando_registros(data, habito, cumprido, humor, obs)
        
        elif opcao == "2":
            listando_registros()
        
        elif opcao == "3":
            listando_registros()
            try:
                id_registro = int(input("Digite o ID do registro para atualizar: "))
                campo = input("Campo a atualizar (data/habito/cumprido/humor/observacoes): ")
                novo_valor = input(f"Novo valor para {campo}: ")
                atualizando_registro(id_registro, {campo: novo_valor})
            except ValueError:
                print("ID Inválido!")
        
        elif opcao == "4":
            listando_registros()
            try:
                id_registro = int(input("Digite o ID do registro para deletar: "))
                deletando_registro(id_registro)
            except ValueError:
                print("ID Inválido!")

        elif opcao == "5":
            print("Saindo...")
            break
        
        else:
            print("Opção Inválida! Tente Novamente")