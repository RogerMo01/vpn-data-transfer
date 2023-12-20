import socket
from udp import recive as udp_recive

def udp_server(host, port, buffer_size=1024):
    server_addr = (host, port)
    
    print(f"UDP server listening on {host}:{port}")
    udp_recive(server_addr, buffer_size)

if __name__ == "__main__":
    udp_server("127.0.0.1", 44450)
