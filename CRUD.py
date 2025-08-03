
#CRUD - Básico
import os
import json
import datetime

from colorama import Fore, Back, Style, init
init(autoreset=True)

lista_atividades = []
contador = 0
contador_concluida = 0


#SALVAR

ARQUIVO = "tarefas.json"

def salvar():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(lista_atividades, f, indent=2, ensure_ascii=False)

def carregar():
    global lista_atividades, contador, contador_concluida
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            lista_atividades = json.load(f)
        for t in lista_atividades:
            if t["Feito"] == "sim":
                contador_concluida += 1
            else:
                contador += 1

#CRUD

def menu():
    print(f"""
          
    ====== Lista To-Do ====== 
          
    Atividades não Concluídas: {contador}
    Atividades Concluídas: {contador_concluida}

    1. Ver Atividades
    2. Adicionar Atividades
    3. Editar Atividades
    4. Excluir Atividades
    5. Salvar e Sair
    """)
   
    
def adicionar_atividade():
    global contador, now, atividadeNova
    
    done = False
    now = datetime.datetime.now().strftime("%Y/%m/%d")
    
    while(done != True):
        atividadeNova = input("Adicione uma atividade: ").capitalize()
        

        if(len(atividadeNova) == 0):
            print("[ERRO] Nenhuma Atividade Inserida")
        
        else:
            vencimento = input("Data de vencimento (YYYY-MM-DD ou vazio): ").strip() or "Nenhuma data Inserida"
            lista_atividades.append({
                "Atividade": atividadeNova, 
                "Vencimento": vencimento, 
                "Feito": "não", 
                "Criada em": now
                })
                
            print(f"Atividade {atividadeNova} adicionada!")
            contador += 1
            
            done = input("Deseja adicionar mais alguma atividade? (s/n): ").lower().strip()
        
            if(done == "s"):
                done = False
            elif(done == "n"):
                print("Retornando...")
                listar_atividades()
                done = True
            else:
                print("[ERRO] Insira 's' ou 'n' ")
                done = True
    

def listar_atividades():
    if not lista_atividades:
        print("Nenhuma tarefa encontrada...")
        return
    else:
        for i, t in enumerate(lista_atividades, 1):
            cor = Fore.GREEN if t["Feito"] == "sim" else Fore.YELLOW
            print(f"{cor}{i}. {t['Atividade']} (Criada em: {t['Criada em']} | Vence em: {t['Vencimento']}) | (Concluida: {t['Feito']})\n")
            
def editar_atividades():
    global contador, contador_concluida
    
    
    if not lista_atividades:
        print("Não existe tarefas para editar...")
    else:
        listar_atividades()
        num = int(input("Insira o número da Atividade que deseja editar: "))
        
        if(num > len(lista_atividades) or num == 0):
            print("Insira um número de Atividade válido...")
            return
        else:
            t = lista_atividades[num - 1]
            
            confirm = input(f"Deseja mudar o nome da Atividade {num}? (s/n)").lower()
            
            if(confirm == "s"):
                novoT = input("Nome novo da Tarefa: ")
                t['Atividade'] = novoT
                print(f"Novo nome de Atividade {novoT} atualizado!")
                
            done = input(f"Atividade concluída? (s/n) ").lower()
            if(done == "s"):
                if(t['Feito'] == "sim"):
                    print("[ERRO] atividade já concluida")
                else:
                    t['Feito'] = "sim"
                    print("Tarefa atualizada!")
                    contador_concluida += 1
                    contador -= 1
            elif(done == "n"):
                if(t['Feito'] == "sim"):
                    t['Feito'] = "não"
                    contador_concluida -= 1
                    contador += 1
            else:
                print("[ERRO] Insira uma das alternativas")
            
                
                

def deletar_atividades():
    global contador
    
    if not lista_atividades:
        print("Nenhuma tarefa para deletar...")
        return
    else:
        done = False
        while(done != True):
            listar_atividades()
            idx = int(input(f"""
    Insira o número da Atividade que vc deseja deletar:
    Ou insira o número 0 para cancelar: """))
            

            if(idx == 0):
                done = True
            else:            
                if(idx > len(lista_atividades)):
                    print("Essa atividade não existe...")
                else:
                    lista_atividades.pop(idx - 1)
                    print(f"Atividade '{idx}' Deletada com sucesso!")
                    contador -= 1
                    
                    done = input("Deseja deletar mais alguma atividade? (s/n): ").lower()
                    
                    if(done == "s"):
                        if not lista_atividades:
                            print("Não existe Atividades para deletar")
                            done = True
                        else:
                            done = False
                    elif(done == "n"):
                        done = True
                    else:
                        print("Insira uma das alternativas")
            

def main():
    carregar()
    
    while True:
        menu()
        op = input("Escolha uma opção: ").strip()
        if op == '1':
            listar_atividades()
        elif op == '2':
            adicionar_atividade()
        elif op == '3':
            editar_atividades()
        elif op == '4':
            deletar_atividades()
        elif op == '5':
            salvar()
            print("Até mais!")
            break
        else:
            print("Opção inválida.")

if __name__ == '__main__':
    main()

