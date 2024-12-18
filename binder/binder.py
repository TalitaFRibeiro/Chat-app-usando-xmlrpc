import xmlrpc.server
porta=5000

#Dicionário

address = 'localhost'

class Binder:
    def __init__(self):
        self.procedure_registry = {}

    def register_procedure(self,procedure_name, address, port):
        self.procedure_registry[procedure_name] = [port,address]
        print(f"Procedimento {procedure_name} registrado na porta {port} e no endereço {address}")
        return True
    
    # def register__instance(self,instance_name, address,port):
    #     self.procedure_registry[instance_name] = [port,address]
    #     print(f" {instance_name} registrada na porta {port} e no endereço {address}")
    #     return True
        

    def lookup_procedure(self,procedure_name):
        return self.procedure_registry.get(procedure_name)

if __name__ == "__main__":
    binder= Binder()
    # Criar servidor xml-rpc
    # binder_server = xmlrpc.server.SimpleXMLRPCServer(('localhost',porta))
    print("Binder pronto e aguardando registros na porta 5000")

    #Registra funções
    binder = xmlrpc.server.SimpleXMLRPCServer(('localhost',porta))
    binder.register_instance(Binder())
    cliente_server = xmlrpc.client.ServerProxy(f'http://{address}:{porta}')

    cliente_server.register_procedure("register_procedure", address, porta)
    cliente_server.register_procedure("lookup_procedure", address, porta)

    #binder_server.register_function(register_procedure, "register_procedure")
    #binder_server.register_function(lookup_procedure,"lookup_procedure")

    binder.serve_forever()