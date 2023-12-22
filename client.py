import socket
from udp import build_packet as udp_send
from udp import build_packet

CLIENT_IP = ('127.0.0.1', 8080)

def run_client(target_host, target_port):
    server_addr = (target_host, target_port)

    while True:
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

        try:
            message = input("> ")
            
            if(message == 'exit'): 
                break
            
            packet = build_packet(message, server_addr, CLIENT_IP)
            raw_socket.sendto(packet, server_addr)

        except KeyboardInterrupt:
            pass
        finally:
            raw_socket.close()


if __name__ == "__main__":
    TARGET_HOST = '127.0.0.2'
    TARGET_PORT = 9090

    run_client(TARGET_HOST, TARGET_PORT)
