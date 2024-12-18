from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import datetime
import xmlrpc.server

port = 8000

binder = xmlrpc.client.ServerProxy("http://localhost:5000")

lista_rooms =[]
class Sala_de_chat:
    def __init__(self):
        self.name = ""
        self.users = []
        self.rooms = []
        self.users = []
        #self.binder = xmlrpc.client.ServerProxy(binder_address)
        self.mensagem = []

    def set_name(self, room_name):
        self.set_name = room_name
    def get_name(self):
        name = self.name
        return name
    def adicionar_mensagem(self,username, room_name, message, tipo):
        msg = {
            "conteudo": message,
            "tipo": tipo,
            "origem": username,
            "destino": room_name,
            "timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        sala = self.rooms[room_name]
        sala.mensagem.append(msg)
    def get_last_fifty(self):
        mensagens_fif = self.mensagem[-50:]
        return mensagens_fif
    
    def get_list_users(self):
        if len(self.users) == 0:
            return "Não há ninguém nessa sala"
        else:
            return self.users
        
        
class Sala_gerente:
    def __init__(self):
        self.total_rooms = 0
        self.rooms = {}
        self.empty_rooms = 0
        self.next_port = 8002 

    def list_users(self,room_name):
        room=self.rooms[room_name]
        lista_user = room.get_list_users()
        return lista_user
    
    # def create_room(self,room_name):
    #     sala = Sala_de_chat()
    #     sala.set_name(room_name)
    #     self.total_rooms += 1
    #     self.rooms[room_name] = sala

    def create_room(self, room_name):
        """Cria uma nova sala e inicia um servidor XML-RPC para ela."""
        if room_name in self.rooms:
            return "Sala já existe."

        # Cria uma nova sala
        new_room = Sala_de_chat()
        self.rooms[room_name] = new_room
        new_room.set_name(room_name)
        print(f'Nova sala {room_name} criada!')
        

        # Registra o servidor da sala em uma nova porta
        room_port = self.next_port
        self.next_port += 1

        def start_room_server():
            """Inicia um servidor XML-RPC para a sala."""
            room_server = SimpleXMLRPCServer(("localhost", room_port), allow_none=True)
            room_server.register_instance(new_room)
            print(f"Sala '{room_name}' rodando na porta {room_port}...")
            room_server.serve_forever()

        import threading
        thread = threading.Thread(target=start_room_server)
        thread.daemon = True
        thread.start()

        # Registra a sala no Binder
        binder.register_procedure(room_name, "localhost", room_port)
        return f"Sala '{room_name}' criada na porta {room_port}."
    

    def list_rooms(self):
        count = 0
        for room_iterator in self.rooms:
            room = self.rooms[room_iterator]
            if(room.users == {}):
                count+=1
        return count
    
    def join_room(self,username,room_name):
        room = self.rooms[room_name]
        room.users.append(username)
        print(f"Usuário {username} foi adicionado a sala {room_name} ")
        mensagens = room.get_last_fifty(self)
        lista_usuarios = room.users
        self.send_message(username,room_name,f"{username} entrou na sala {room_name}")
        return mensagens,lista_usuarios
        
        

    def list_users(self,room_name):
        selecionar = self.rooms[room_name]
        return selecionar.users.values()

    def send_message(self,username, room_name, message, recipient=None):
        if(recipient == None):
            tipo = "Broadcast"
        self.rooms[room_name].adicionar_mensagem(username,room_name,message,tipo)
        

    def receive_messages(self,username, room_name):
        sala = self.rooms[room_name]
        if(len(sala.mensagem))

    
        

# class Mensagem:
#     def __init__(self, tipo, username, destinatario, conteudo, timestamp):
#         self.tipo = tipo
#         self.origem = username
#         self.destinatario = destinatario
#         self.conteudo = conteudo
#         self.timestamp = timestamp

    
    
    




    




def list_rooms():
    pass

#def list_users(room_name):

# def room_inicializer(room_name):
#     pass  

if __name__ == "__main__":
    manager = Sala_gerente()
    
    # rpc_server = SimpleXMLRPCServer(('localhost', 8000))
    rpc_server = xmlrpc.server.SimpleXMLRPCServer(('localhost', port))
    rpc_server.register_introspection_functions()
    
    rpc_server.register_instance(Sala_gerente())
    rpc_server.register_instance(Sala_de_chat())
    print("Chat server running on port 8000...")
    rpc_client = xmlrpc.client.ServerProxy('http://localhost:5000')
    rpc_client.
    

    rpc_server.serve_forever()
