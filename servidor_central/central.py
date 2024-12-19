from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
from datetime import datetime
import xmlrpc.server

port = 8000



lista_rooms =[]
class Sala_de_chat:
    def __init__(self,name):
        self.name = name
        self.users = []
        self.mensagem = []

    # def adicionar_mensagem(self, username, room_name, message, tipo):
    #     # msg = {
    #     #     "conteudo": message,
    #     #     "tipo": tipo,
    #     #     "origem": username,
    #     #     "destino": room_name,
    #     #     "timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     # }
    #     if(tipo == "Broadcast"):
    #         self.mensagem.append(msg)
        

    def get_last_fifty(self):
        mensagens_fif = self.mensagem[-50:]
        return mensagens_fif
    
        
    def sair_sala(self,username):
        self.users.pop(username)
        print(f"Usuário {username} foi excluído")
        
        
class Sala_gerente:
    def __init__(self):
        self.total_rooms = 0
        self.rooms = {}
        self.empty_rooms = 0
        self.next_port = 8002 
        self.users=[]

    
    # def create_room(self,room_name):
    #     sala = Sala_de_chat()
    #     sala.set_name(room_name)
    #     self.total_rooms += 1
    #     self.rooms[room_name] = sala

    def criar_sala(self, room_name):
        """Cria uma nova sala e inicia um servidor XML-RPC para ela."""
        for i in self.rooms:
            sala = self.rooms[i]
            if sala.name == room_name:
                return "Sala ja existe"

        # Cria uma nova sala
        new_room = Sala_de_chat(room_name)
        self.rooms[room_name] = new_room
        return f'Sala {new_room.name} criada!'
        
    # def criar_usuario(self,username,porta):
    #     usuario = xmlrpc.client.ServerProxy('http://localhost:{porta}')
    #     usuario.username = username
       

#        # Registra a sala no Binder
#        binder.register_procedure(room_name, "localhost", room_port)
#        return f"Sala '{room_name}' criada na porta {room_port}."
    

    def listar_salas(self):
        return list(self.rooms)
    
    def esta_em_alguma_sala(self,username):
        for i in self.rooms:
            sala = self.rooms[i]
            for i in sala.users:
                if i.username == username:
                    return True
        return False
    


    def entrar_sala(self,username,room_name):
        if(room_name in self.rooms == False):
            return "Sala não existe."
        for i in self.rooms:
            sala = self.rooms[i]
            if sala.name == room_name:
                room = sala
        
        user=self.find_user(username)
        if(user == False):
            return "Usuário nao existe"
        else:
            
            room.users.append(user) #adicionar o usuário na sala
            print(f"Usuário {user.username} foi adicionado a sala {room_name} ")
            mensagens = room.get_last_fifty()
            for pessoa in room.users:
                pessoa.enviar_mensagem_privada(username,room_name,f"{username} entrou na sala {room_name}")
            user.enviar_mensagem(username,room_name,mensagens, username)
        
        
    def find_user(self,username):
        for i in self.users:
            user_temp = self.users[i]
            if username in user_temp.username:
                return user_temp
        return False
    def criar_username(self,username):
        for i in self.users:
            user_temp = self.users[i]
            if username in user_temp.username:
                return "Usuário ja cadastrado"
        
        user = Cliente(username)
        self.users.append(user)
        return "Usuário cadastrado com sucesso"
        
    def achar_sala(self,room_name):
        for i in self.rooms:
            sala = self.rooms[i]
            if sala.name == room_name:
                return sala
        return None
    
    def deletar_sala(self,room_name):
        for i in self.rooms:
            sala = self.rooms[i]
            if sala.name == room_name:
                self.rooms.pop(room_name)
                del sala
                return "Sala deletada com sucesso"
        return "Sala nao encontrada"

    def listar_usuarios(self,room_name):
        selecionar = self.rooms[room_name]
        return list(selecionar.users)

    def enviar_mensagem(self,username, room_name, message, recipient=None): #username da pessoa q enviou a msg
        
        if(recipient == None):
            tipo = "Broadcast"
            msg = {
            "conteudo": message,
            "tipo": tipo,
            "origem": username,
            "destino": room_name, #todos os usuários da sala
            "timestamp":  datetime.now().strftime("%d-%m-%Y- %H:%M:%S")
            }
            sala = self.achar_sala(room_name)
            sala.adicionar_mensagem(username,room_name,message)
            for pessoa in sala.users:
                pessoa.receber_mensagem_privada(username,room_name,msg)
        else:
            tipo = "Unicast"
            msg = {
            "conteudo": message,
            "tipo": tipo,
            "origem": username,
            "sala": room_name,
            "destino": recipient,
            "timestamp":  datetime.now().strftime("%d-%m-%Y- %H:%M:%S")
            }
            for usuario in self.users:
                if(usuario.username == recipient):
                    usuario.receber_mensagem_privada(username,room_name,msg)

    def username_existe(self,username):
        for i in self.rooms:
            sala = self.rooms[i]
            for i in sala.users:
                if i.username == username:
                    return True
        return False

    def username_esta_em_sala(self,username,room_name):
        sala = self.rooms[room_name]
        for i in sala.users:
            if i.username == username:
                return True
        return False

        

    # def receber_mensagens(self,username, room_name):
    #     if username not in self.rooms[room_name].users:
    #         return "Usuário não está na sala."
        
    #     sala = self.rooms[room_name]
    #     # return [msg for msg in sala.mensagem if msg["timestamp"] > timestamp]
    #     return sala.mensagem
        



class Cliente:
    def __init__(self,username):
        self.username = username
        self.mensagem = []
        self.origem_sala = ""

        self.tamanho_vetor_mensagem = 0
    
    def receber_mensagem_privada(self,username, room_name, message):
        self.mensagem.append(message)  
        self.origem_sala = room_name

         
        

# class Mensagem:
#     def __init__(self, tipo, username, destinatario, conteudo, timestamp):
#         self.tipo = tipo
#         self.origem = username
#         self.destinatario = destinatario
#         self.conteudo = conteudo
#         self.timestamp = timestamp

    
    
    






#def list_users(room_name):

# def room_inicializer(room_name):
#     pass  

if __name__ == "__main__":
    cliente = Cliente("test")
    manager = Sala_gerente()
    sala_modelo = Sala_de_chat("teste")
    
    # rpc_server = SimpleXMLRPCServer(('localhost', 8000))
    rpc_server = xmlrpc.server.SimpleXMLRPCServer(('localhost', port))
    #rpc_server.register_introspection_functions()
 #   rpc_server.register_function(sala_modelo.adicionar_mensagem,"adiciona_mensagem") #Pra poder registrar o método de "Sala_de_chat"
    rpc_server.register_function(sala_modelo.sair_sala,"sair_sala")
    rpc_server.register_function(cliente.receber_mensagem_privada,"receber_mensagem_privada")
#    rpc_server.register_function(sala_modelo.get_last_fifty,"ultimos_cinquenta")
    rpc_server.register_instance(Sala_gerente())
    # rpc_server.register_instance(Sala_de_chat())
    print("Chat server running on port 8000...")
    rpc_client = xmlrpc.client.ServerProxy('http://localhost:5000')
    # rpc_client.register_procedure('adicionar mensagem','localhost',port)
    rpc_client.register_procedure('Entrar na sala','localhost',port)
    rpc_client.register_procedure('Sair da sala','localhost',port)
    rpc_client.register_procedure('Enviar mensagem','localhost',port)
    rpc_client.register_procedure('Listar usuários','localhost',port)
    #rpc_client.register_procedure('Receber mensagens','localhost',port)
    rpc_client.register_procedure('Listar salas','localhost',port)
    rpc_client.register_procedure('Criar sala','localhost',port)
    rpc_client.register_procedure('Deletar sala','localhost',port)


    rpc_server.serve_forever()
