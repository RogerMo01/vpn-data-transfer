import socket
# from udp import build_packet
from unsecure_udp import build_packet

CLIENT_ADDR = ('127.0.0.2', 8080)
TARGET_ADDR = ('127.0.0.100', 9090)
SERVER_ADDR = ('127.0.0.3', 8888)

def run_client():
    while True:
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

        try:
            message = input("> ")
            
            if(message == 'exit'): 
                break
            
            packet = build_packet(message, TARGET_ADDR, CLIENT_ADDR)
            raw_socket.sendto(packet, TARGET_ADDR)

        except KeyboardInterrupt:
            pass
        finally:
            raw_socket.close()


if __name__ == "__main__":
    run_client()