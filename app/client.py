import socket
import threading


SERVER_IP = "127.0.0.1"  # Placeholder
TCP_PORT = 5001




nickname = input("Choose a nickname: ")

#TCP client socket
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('localhost', 5555))
client.send(nickname.encode('ascii'))


def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))

            else:
                print(message)


        except:
            print("An error occured")
            break

    client.close()



def write():
    while True:
        try:
            message = f'{nickname}: {input("")}'

            if message.lower() == '/exit':
                client.send(f"{nickname} has left the chat.".encode('ascii'))
                print("Disconnecting from chat...")
                client.close()
                break

            else:
                client.send(message.encode('ascii'))

        except:
            break

    client.close()
    print("Client disconnected from chat")


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()