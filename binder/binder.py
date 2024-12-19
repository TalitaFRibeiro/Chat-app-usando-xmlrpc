import xmlrpc.server
import xmlrpc.client
porta=5000

#Dicionário

address = 'localhost'

class Binder:
    def __init__(self):
        self.procedure_registry = {}

    def register_procedure(self,procedure_name, address, port):
        self.procedure_registry[procedure_name] = [port,address]
        print(f'Procedimento {procedure_name} registrado na porta {port} e no endereço {address}')
        return True
    
    # def register__instance(self,instance_name, address,port):
    #     self.procedure_registry[instance_name] = [port,address]
    #     print(f" {instance_name} registrada na porta {port} e no endereço {address}")
    #     return True
    def show_procedures(self):
        return list(self.procedure_registry)

    def lookup_procedure(self,procedure_name):
        return self.procedure_registry.get(procedure_name)

if __name__ == "__main__":
    binder= Binder()
    #binder.register_procedure("Registrar procedimento", address, porta)
    #binder.register_procedure("Chamar procedimento", address, porta)
    #binder.register_procedure("Mostrar procedimentos", address, porta)

    #Registra funções
    binder_server = xmlrpc.server.SimpleXMLRPCServer(('localhost',porta))
    binder_server.register_instance(binder)
    print("Binder pronto e aguardando registros na porta 5000")
    binder_server.serve_forever()