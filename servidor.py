import socket
import threading

HOST = 'localhost'
PORT = 8080

dic_usuarios = {}

def broadcast(cliente_remetente, mensagem):
    for cliente in dic_usuarios.keys():
            if cliente == cliente_remetente:
                pass

            else:
                cliente.send(mensagem.encode('utf-8'))

def receber_mensagem(cliente):
   
   while True:
        
        mensagem = cliente.recv(1024).decode('utf-8')

        if not mensagem:
            broadcast(cliente, f"{dic_usuarios[cliente]} desconectou-se do chat.")
            print(f"{dic_usuarios[cliente]} desconectou-se do servidor.")
            dic_usuarios.pop(cliente)
            cliente.close()

            break
        else:
            mensagem_cliente = f"{dic_usuarios[cliente]}: {mensagem}"
            broadcast(cliente, mensagem_cliente)
         
servidor = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind((HOST, PORT))
servidor.listen()
print("Aguardando conexões...")

try:
    while True:
        try:  
            cliente, addr =  servidor.accept()
            print(f"Cliente {addr} conectou-se ao servidor")

            #print(cliente)

            cliente.send('NICK'.encode('utf-8'))
            nickname = cliente.recv(1024).decode('utf-8')

            dic_usuarios[cliente] = nickname

            broadcast(cliente, f"{nickname} entro no chat.")

            thread_cliente = threading.Thread(target = receber_mensagem, args = [cliente], daemon= True).start()

        except OSError:
            print("\nEncerrando recebimento de novos clientes")
            cliente.close()
        
except KeyboardInterrupt:
    print("\nDesligando servidor...")
    servidor.close()



