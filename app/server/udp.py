import socket
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# UDP Server for Status Notifications
def udp_server():
    udp_ip = "127.0.0.1"
    udp_port = 8081
    buffer_size = 1024

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((udp_ip, udp_port))

    logging.info(f"UDP Server is running on {udp_ip}:{udp_port}...")


    while True:
        try:
            message, addr = server.recvfrom(buffer_size)
            decoded_msg = message.decode()
            print(f"Received message from {addr}: {decoded_msg}")
            
            # Process the message (status update)
            if message.decode().startswith("STATUS:"):
                _, sender, status = decoded_msg.split(":", 2)
                #print(f"{sender} is {status}")
                logging.info(f"Typing status update from {addr}: {message}")

            else:
                logging.warning(f"Invalid UDP message format from {addr}")

        except Exception as e:
            logging.error(f"Error in UDP server: {e}")
            break



if __name__ == "__main__":
    udp_server()
