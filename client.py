import socket
from udp import send as udp_send
from udp import recive as udp_recive

CLIENT_IP = ('127.0.0.1', 8080)

def run_client(target_host, target_port):
    server_addr = (target_host, target_port)

    while True:
        client_recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        client_recv_socket.bind(CLIENT_IP)

        try:
            message = input("> ")
            
            if(message == 'exit'): 
                break

            udp_send(message, server_addr, CLIENT_IP)

        except KeyboardInterrupt:
            pass
        finally:
            client_recv_socket.close()


if __name__ == "__main__":
    TARGET_HOST = "127.0.0.2"
    TARGET_PORT = 9090

    run_client(TARGET_HOST, TARGET_PORT)
