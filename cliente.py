import socket
import threading

HOST = 'localhost'
PORT = 8080

def escutar(cliente):

    while True:

        mensagem = cliente.recv(1024).decode('utf-8')
        
        if not mensagem:
            print("O servidor parou de responder")
            cliente.close()
            break

        else:
            print(mensagem)

def enviar():

    try:
        while True:

            mensagem = input("")

            try:
                cliente.send(mensagem.encode('utf-8'))

            except OSError:
                #cliente.close()
                print("Desconectando...")
                break

    except KeyboardInterrupt:
        print("\nVocê desconectou-se")
        cliente.close()

cliente = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM)
cliente.connect((HOST, PORT))   

thread_cliente = threading.Thread(target = escutar, args = [cliente], daemon=True).start()

print("--- Conectado ao chat ---")
enviar()

