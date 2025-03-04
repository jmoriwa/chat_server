import socket
import threading
import logging


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# Server configuration
TCP_IP = "127.0.0.1"
TCP_PORT = 8082
BUFFER_SIZE = 1024

clients = []  # List to keep track of connected clients

def handle_client(conn, addr):
    """Handles communication with a single client."""
    
    print(f"New connection from {addr}")
    clients.append(conn)
    nickname = conn.recv(BUFFER_SIZE).decode()

    while True:
        try:
            message = conn.recv(BUFFER_SIZE).decode()
            if not message:
                break 

            clients[conn] = nickname
            
            logging.info(f"Message from {nickname}: {message}")
            broadcast(message, conn)

        except ConnectionResetError:
            logging.warning(f"Connection reset by {nickname} ({addr}).")
            break
            
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
            break

    print(f"Client {addr} disconnected.")
    if conn in clients:
        clients.remove(conn)
    conn.close()

def broadcast(message, sender_conn):
    """Sends a message to all clients except the sender."""
    for client in clients[:]:  # Iterate over a copy to avoid modifying the list while iterating
        if client != sender_conn:
            try:
                client.send(message.encode())
            except:
                print(f"Client {client} disconnected unexpectedly. Removing from list.")
                client.close()
                clients.remove(client)

def tcp_server():
    """Starts the multithreaded TCP server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((TCP_IP, TCP_PORT))
    server.listen()

    logging.info(f"TCP Server is running on {TCP_IP}:{TCP_PORT}...")

    while True:
        try:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
        except Exception as e:
            logging.error(f"Error accepting connection: {e}")

            
if __name__ == "__main__":
    tcp_server()
