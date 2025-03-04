import socket
import threading
import os
import time
from pynput import keyboard


SERVER_IP = "127.0.0.1"  # Placeholder
TCP_PORT = 8082
UDP_PORT = 8081
BUFFER_SIZE = 1024



nickname = input("Choose a nickname: ")

#TCP client socket
tcp_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcp_client.connect((SERVER_IP, TCP_PORT))
tcp_client.send(f"{nickname} has joined the chat ".encode('ascii'))


#UDP client socket for short messages
udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


last_typing_time = 0

def send_status(status):
    """Sends 'is typing...' updates over UDP"""
    udp_client.sendto(f"STATUS:{nickname} : {status}.".encode('ascii'), (SERVER_IP, UDP_PORT))


def detect_typing():
    """Detects keyboard activity and sends 'typing' status"""
    global last_typing_time

    def on_press(key):
        global last_typing_time
        current_time = time.time()
        
        # Send typing status only if enough time has passed to avoid spam
        if current_time - last_typing_time > 2:
            send_status("typing...")
            last_typing_time = current_time

    listener = keyboard.Listener(on_press=on_press)
    listener.start()



def receive_tcp():
    while True:
        try:
            message = tcp_client.recv(BUFFER_SIZE).decode('ascii')
            if message:
                print(message)


        except:
            print("An error occured")
            tcp_client.close()
            break

    

def receive_udp():
    """Receives status updates from the server via UDP."""
    while True:
        try:
            data, _ = udp_client.recvfrom(BUFFER_SIZE)
            print(data.decode('ascii'))  # Display status updates
        except:
            break



def write():
    while True:
        try:
            msg_content = input("")
            
            if msg_content.lower() == "/exit":
                tcp_client.send(f"{nickname} has left the chat".encode('ascii'))
                print("Disconnecting from chat...")
                tcp_client.close()
                break
                '''
                elif msg_content.lower() == "/typing":
                    send_status("typing...")
                '''
            else:
                tcp_client.send(f"{nickname}: {msg_content}".encode('ascii'))
        
        except:
            break

    print("Client disconnected from chat")


def send_file(filename):
    """Sends a file to the server over TCP."""
    try:
        file_size = os.path.getsize(filename)
        tcp_client.send(f"FILE:{nickname}:{filename}:{file_size}".encode())

        with open(filename, "rb") as f:
            while (data := f.read(BUFFER_SIZE)):
                tcp_client.send(data)
        
        print(f"File '{filename}' sent successfully.")

    except FileNotFoundError:
        print(f"File '{filename}' not found.")



receive_thread = threading.Thread(target=receive_tcp)
receive_thread.start()

udp_receive_thread = threading.Thread(target=receive_udp, daemon=True)
udp_receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()