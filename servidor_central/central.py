from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import datetime
import xmlrpc.server

port = 8000



lista_rooms =[]
class Sala_de_chat:
    def __init__(self,name):
        self.name = name
        self.users = []
        self.mensagem = []

    def adicionar_mensagem(self, username, room_name, message, tipo):
        msg = {
            "conteudo": message,
            "tipo": tipo,
            "origem": username,
            "destino": room_name,
            "timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.mensagem.append(msg)

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

    
    # def create_room(self,room_name):
    #     sala = Sala_de_chat()
    #     sala.set_name(room_name)
    #     self.total_rooms += 1
    #     self.rooms[room_name] = sala

    def criar_sala(self, room_name):
        """Cria uma nova sala e inicia um servidor XML-RPC para ela."""
        if room_name in self.rooms:
            return "Sala já existe."

        # Cria uma nova sala
        new_room = Sala_de_chat(room_name)
        self.rooms[room_name] = new_room
        return f'Sala {room_name} criada!'
        
    # def criar_usuario(self,username,porta):
    #     usuario = xmlrpc.client.ServerProxy('http://localhost:{porta}')
    #     usuario.username = username
       

#        # Registra a sala no Binder
#        binder.register_procedure(room_name, "localhost", room_port)
#        return f"Sala '{room_name}' criada na porta {room_port}."
    

    def listar_salas(self):
        return list(self.rooms)
    
    def entrar_sala(self,username,room_name):
        room = self.rooms[room_name]
        if username in room.users:
            return "Usuário já está na sala"
        print(f"Usuário {username} foi adicionado a sala {room_name} ")
        mensagens = room.get_last_fifty(self)
        lista_usuarios = room.users
        self.send_message(username,room_name,f"{username} entrou na sala {room_name}")
        return mensagens,lista_usuarios
        
        

    def listar_usuarios(self,room_name):
        selecionar = self.rooms[room_name]
        return list(selecionar.users)

    def enviar_mensagem(self,username, room_name, message, recipient=None):
        if(recipient == None):
            tipo = "Broadcast"
        self.rooms[room_name].adicionar_mensagem(username,room_name,message,tipo)

    


        

    def receber_mensagens(self,username, room_name):
        if username not in self.rooms[room_name].users:
            return "Usuário não está na sala."
        
        sala = self.rooms[room_name]
        # return [msg for msg in sala.mensagem if msg["timestamp"] > timestamp]
        return sala.mensagem
        

    
        

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
    manager = Sala_gerente()
    sala_modelo = Sala_de_chat("teste")
    
    # rpc_server = SimpleXMLRPCServer(('localhost', 8000))
    rpc_server = xmlrpc.server.SimpleXMLRPCServer(('localhost', port))
    #rpc_server.register_introspection_functions()
 #   rpc_server.register_function(sala_modelo.adicionar_mensagem,"adiciona_mensagem") #Pra poder registrar o método de "Sala_de_chat"
    rpc_server.register_function(sala_modelo.sair_sala,"sair_sala")
#    rpc_server.register_function(sala_modelo.get_last_fifty,"ultimos_cinquenta")
    rpc_server.register_instance(Sala_gerente())
    # rpc_server.register_instance(Sala_de_chat())
    print("Chat server running on port 8000...")
    rpc_client = xmlrpc.client.ServerProxy('http://localhost:5000')
    rpc_client.register_procedure('adicionar_mensagem','localhost',port)
    rpc_client.register_procedure('entrar_sala','localhost',port)
    rpc_client.register_procedure('sair_sala','localhost',port)
    rpc_client.register_procedure('enviar_mensagem','localhost',port)
    rpc_client.register_procedure('listar_usuarios','localhost',port)
    rpc_client.register_procedure('receber_mensagens','localhost',port)
    rpc_client.register_procedure('listar_salas','localhost',port)
    rpc_client.register_procedure('criar_sala','localhost',port)


    rpc_server.serve_forever()
