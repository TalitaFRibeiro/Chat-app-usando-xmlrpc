
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


def recebe_mensagem(server, username, room_name, interval=2):
    def fetch_messages():
        while True:
            try:

                # Chama o método remoto para receber mensagens
                new_messages = server.receber_mensagem_privada(username, room_name)

                # Exibe as mensagens recebidas
                for message in new_messages:
                    print(f"[{message['timestamp']}] {message['origem']}: {message['conteudo']}")
            except Exception as e:
                print(f"Erro ao buscar mensagens: {e}")

            # Aguarda o próximo ciclo
            time.sleep(interval)

    # Cria e inicia uma thread para buscar mensagens
    thread = threading.Thread(target=fetch_messages, daemon=True)
    thread.start()

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
    if(server.criar_sala("Sala teste")=="Sala ja existe"):
        print("Sala ja existe")

    for sala in range(len(server.listar_salas())):    
        print(sala)
    print(f"Salas:{server.listar_salas()}\n")
    server.entrar_sala(username, "Sala teste")
    print(server.listar_usuarios("Sala teste"))

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
  

