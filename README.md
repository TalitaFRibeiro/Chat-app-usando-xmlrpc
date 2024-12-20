### Chat-app-usando-xmlrpc

Esse é um aplicativo de chat usando a biblioteca xmlrpc no python. 

# Para iniciar, é preciso ir até o diretório de cada arquivo e chamar python3 arquivo.py.
A ordem de execução da ligação dos servidores é primeiro lugar o binder, pois ele que registra as funções; segundo, é necessário ligar o servidor_central, nele é onde estão as implementações das funções que serão registradas no binder e que fazem parte do funcionamento dos serviços do servidor; depois, rodar o código do cliente no diretório dele,python3 cliente.py.