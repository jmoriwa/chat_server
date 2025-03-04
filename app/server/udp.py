import socket

# UDP Server for Status Notifications
def udp_server():
    udp_ip = "127.0.0.1"
    udp_port = 8081
    buffer_size = 1024

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((udp_ip, udp_port))

    print(f"UDP Server is listening on {udp_ip}:{udp_port} for status notifications...")

    while True:
        try:
            message, addr = server.recvfrom(buffer_size)
            decoded_msg = message.decode()
            print(f"Received message from {addr}: {decoded_msg}")
            
            # Process the message (status update)
            if message.decode().startswith("STATUS:"):
                _, sender, status = decoded_msg.split(":", 2)
                print(f"{sender} is {status}")

            else:
                print("Invalid UDP message format.")

        except Exception as e:
            print(f"UDP Server error: {e}")
            break



if __name__ == "__main__":
    udp_server()
