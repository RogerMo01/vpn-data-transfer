import socket
from udp import send as udp_send

def run_client(target_host, target_port):
    server_addr = (target_host, target_port)

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP) as client_socket:
            client_socket.connect(server_addr)

            message = input()
            
            if(message == 'exit'): 
                break

            print(f"[*] Sending message to {target_host}:{target_port}: {message}")
            udp_send(message, server_addr)

if __name__ == "__main__":
    TARGET_HOST = "127.0.0.1"
    TARGET_PORT = 9090

    run_client(TARGET_HOST, TARGET_PORT)
