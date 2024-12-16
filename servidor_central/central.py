from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import datetime
import xmlrpc.server

port = 8000

lista_rooms =[]
class Sala_de_chat:
    def __init__(self,binder_address):
        self.name = ""
        self.users = []
        self.rooms = []
        self.users = {}
        self.binder = xmlrpc.client.ServerProxy(binder_address)
        self.mensagem = []
    def set_name(self, room_name):
        self.set_name = room_name
    def get_name(self):
        name = self.name
        return name
    def list_users(self,room_name):
        if self.users == {}:
            return "Não há ninguém nessa sala"
        
class Sala_gerente:
    def __init__(self):
        self.total_rooms = 0
        self.rooms = {}
        self.empty_rooms = 0
    
    def create_room(self,room_name):
        sala = Sala_de_chat()
        sala.set_name(room_name)
        self.total_rooms += 1
        self.rooms[room_name] = sala

    
    def list_rooms(self):
        count = 0
        for room_iterator in self.rooms:
            room = self.rooms[room_iterator]
            if(room.users == {}):
                count+=1
        return count

    def list_users(self,room_name):
        selecionar = self.rooms[room_name]
        return selecionar.users.values()

    def send_message(self,username, room_name, message, recipient=None):
        if(recipient == None):
            tipo = "Broadcast"
        msg = {
            "conteudo": message,
            "tipo": tipo,
            "origem": username,
            "destino": room_name,
            "timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        sala = self.rooms[room_name]
        sala.mensagem.append(msg)
        return "Mensagem enviada"

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
    rpc_server.re
    rpc_server.register_instance(Sala_gerente)
    rpc_server.register_instance(Sala_de_chat)
    print("Chat server running on port 8000...")
    binder = xmlrpc.client.ServerProxy('http://localhost:5000')
    

    rpc_server.serve_forever()
