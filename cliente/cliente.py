
import threading
import xmlrpc.client
import xmlrpc.server
import sys
import time 
port = 5430


        

# Função para realizar as operações de cálculo
# def calcula(calc_server):
#     a = int(input("Digite o primeiro número: "))
#     b = int(input("Digite o segundo número: "))

#     print(f"Soma: {calc_server.soma(a, b)}")
#     print(f"Subtração: {calc_server.subtracao(a, b)}")
#     print(f"Multiplicação: {calc_server.multiplicacao(a, b)}")
#     print(f"Divisão: {calc_server.divisao(a, b)}")

vetor_mensagem=[]
def recebe_mensagem(server, username, room_name, interval=2):
    def fetch_messages():
        while True:
            try:
                usuario = server.find_user(username)
                new_messages = usuario.mensagem
                novas_mensagens = [x for x in vetor_mensagem if x not in new_messages]
                # Chama o método remoto para receber mensagens
                

                # Exibe as mensagens recebidas
                for message in novas_mensagens:
                    print(f"[{message['timestamp']}] {message['origem']}: {message['conteudo']}")
            except Exception as e:
                print(f"Erro ao buscar mensagens: {e}")

            # Aguarda o próximo ciclo
            time.sleep(interval)

    # Cria e inicia uma thread para buscar mensagens
    thread = threading.Thread(target=fetch_messages, daemon=True)
    thread.start()

def mostrar_opcoes(lista_procedimentos):
    print("Escolha uma opção no menu:")
    for i in range(len(lista_procedimentos)):
        print(f"{i+1} - {lista_procedimentos[i]}")

if __name__ == "__main__":


    print("primeiro")

    binder = xmlrpc.client.ServerProxy('http://localhost:5000')
    lista_procedimentos = binder.show_procedures()
    
    print("Escolha uma opção no menu:")
    for i in range(len(lista_procedimentos)):
        
        print(f"{i+1} - {lista_procedimentos[i]}")
    
    opcao = int(input("Digite o número da opção desejada: ")) - 1
    procedure_name = lista_procedimentos[opcao]
    procedure_port, procedure_address = binder.lookup_procedure(procedure_name)
    print(f"Procedimento {procedure_name} registrado na porta {procedure_port} e no endereço {procedure_address}")
    server = xmlrpc.client.ServerProxy(f'http://{procedure_address}:{procedure_port}')

    if server is None:
        print("Oh no!")
        exit(1)
    
    username = input("Digite o seu username: ")
    print(server.username_existe(username))
    try:
        if server.criar_username(username):
            print(f"Username '{username}' registrado com sucesso!")
        else:
            print(f"Username '{username}' já está em uso.")
            exit(1)
    except Exception as e:
        print(f"Erro ao criar username: {e}")
        exit(1)
    mostrar_opcoes(lista_procedimentos)
    # if(server.criar_sala("Sala teste")=="Sala ja existe"):
    #     print("Sala ja existe")

    # for sala in range(len(server.listar_salas())):    
    #     print(sala)
    # print(f"Salas:{server.listar_salas()}\n")
    # server.entrar_sala(username, "Sala teste")

 

    if(opcao == 1): # Entrar na sala
        print("Salas:")
        salas = server.listar_salas()
        if(len(salas) == 0):
            print("Nenhuma sala criada")
        for i in range(len(salas)): 
            print(f"{i+1} - {salas[i]}")
        escolha = input("Digite a escolha da sala: ")
        if(escolha <= len(salas) and escolha > 0 and escolha <= len(salas)):
            room_name = salas[int(escolha)-1].name
        if(server.criar_sala(room_name) == "Sala ja existe"):
            server.entrar_sala(username, room_name)
        # else:
        #     server.criar_sala(room_name)
        #     server.entrar_sala(username, room_name)

    elif(opcao == 2): # Sair sala
        if(server.esta_em_alguma_sala(username)):
            server.sair_sala(username)
        else:
            print("Usuário nao esta em nenhuma sala")
    
    elif(opcao == 3): # Enviar mensagem
        try:
            room_name = input("Digite o nome da sala: ")
            if(server.esta_em_sala(username, room_name)==False):
                
                raise Exception("Usuário nao esta na sala")
            
            message = input("Digite a mensagem: ")
            privada = input("Mensagem privada? (S/N): ")
            if(privada == "S" or privada == "s"):    
                recipient = input("Digite o username do destinatário: ")   
                if(server.username_esta_em_sala(recipient, room_name)==False):
                    raise Exception("Destinatário nao esta na sala")
                server.enviar_mensagem(username, room_name, message, recipient)
            else:
                user_list = server.listar_usuarios(room_name)

                server.enviar_mensagem(username, room_name, message)

        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")

    elif(opcao == 4): # Listar usuários
        try:
            room_name = input("Digite o nome da sala: ")
            if(server.esta_em_sala(username, room_name)==False):
                raise Exception("Usuário nao esta na sala")
            server.listar_usuarios(room_name)
        except Exception as e:
            print(f"Erro ao listar usuários: {e}")

    # elif(opcao == 5): # era receber mensagens
    elif(opcao == 5): # Listar sala
        try:
            room_name = input("Digite o nome da sala: ")
            if(server.esta_em_sala(username, room_name)==False):
                raise Exception("Usuário nao esta na sala")
            server.listar_sala(room_name)
        except Exception as e:
            print(f"Erro ao listar sala: {e}")

    elif(opcao == 6): # Criar sala
        try:
            room_name = input("Digite o nome da sala: ")
            server.listar_sala(room_name)
            if(room_name in server.achar_sala(room_name)):
                raise Exception("Sala ja existe")
            server.criar_sala(room_name)
        except Exception as e:
            print(f"Erro ao criar sala: {e}")


    # Chama a funcao para receber mensagens
    #recebe_mensagem(server, "Usuario", "Sala_de_chat", 2)



    # def criar_username():
    #     username = input("Digite o seu username: ")
    #     clientee = Cliente(username)


    
    

    

    # if calc_server_port is None:
    #     print("Serviço de calculadora não encontrado.")
    #     exit(1)

    # Cria um cliente que se conecta ao servidor de calculadora na porta descoberta
    # calc_server = xmlrpc.client.ServerProxy(f'http://{server_address}:{calc_server_port}')

    # Inicia a thread para buscar mensagens
  

