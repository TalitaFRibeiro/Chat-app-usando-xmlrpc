
import threading
import xmlrpc.client
import xmlrpc.server
import sys
import time 
port = 5430

class Cliente:
    def __init__(self,username):
        self.username = ""
        self.mensagem = []
        self.tamanho_vetor_mensagem = 0
    
    def recebe_mensagem(self,room,msg_arr):
        for msg in msg_arr:
            self.mensagem.append(msg)
            print(f"({msg['tipo']}) {msg['username']} às {msg['timestamp']}:  {msg['texto']}")
        

        
        

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
                new_messages = server.receber_mensagens(username, room_name)

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
    print(f'Metodos disponiveis: {binder.show_procedures()} \t\n')



    # def criar_username():
    #     username = input("Digite o seu username: ")
    #     clientee = Cliente(username)


    
    

    

    # if calc_server_port is None:
    #     print("Serviço de calculadora não encontrado.")
    #     exit(1)

    # Cria um cliente que se conecta ao servidor de calculadora na porta descoberta
    # calc_server = xmlrpc.client.ServerProxy(f'http://{server_address}:{calc_server_port}')

    # Inicia a thread para buscar mensagens
  

