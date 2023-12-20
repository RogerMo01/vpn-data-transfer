import socket
from udp import send as udp_send

def udp_client(host, port, message):
    server_addr = (host, port)

    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP) as client_socket:
        client_socket.connect(server_addr)

        print(f"Sending message to {host}:{port}: {message}")
        udp_send(message, server_addr)

if __name__ == "__main__":
    udp_client("127.0.0.1", 44450, "Hello, Server!")
