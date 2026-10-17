import socket
import threading

HOST = 'localhost'
PORT = 8080

cliente_list = []

def broadcast(cliente, mensagem):
    for cliente in cliente_list:
        cliente.send(mensagem.encode('utf-8'))

def receber_mensagem(cliente):
   
   while True:
        
        mensagem = cliente.recv(1024).decode('utf-8')

        if not mensagem:
            print(f"{addr} desconectou-se do servidor")
            cliente_list.remove(cliente)
            cliente.close()
            break
        else:
            broadcast(cliente, mensagem)
         
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

            cliente_list.append(cliente)

            thread_cliente = threading.Thread(target = receber_mensagem, args = [cliente], daemon= True).start()

        except OSError:
            print("\nEncerrando recebimento de novos clientes")
            cliente.close()
        
except KeyboardInterrupt:
    print("\nDesligando servidor...")
    servidor.close()

