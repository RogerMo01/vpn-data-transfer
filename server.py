import socket
from udp import receive as udp_receive
from udp import send as udp_send


def run_server(bind_host, bind_port):
    server_addr = (bind_host, bind_port)

    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    raw_socket.bind(server_addr)

    print(f"[*] Listening on {bind_host}:{bind_port}")

    while True:
        client_addr, request, valid = udp_receive(raw_socket, 1024)
        
        if(not valid):
            print(f"[*] {request}")
        else:
            print(f"[*] {client_addr} says: {request}")

    raw_socket.close()
    

if __name__ == "__main__":
    BIND_HOST = "127.0.0.2"
    BIND_PORT = 9090

    run_server(BIND_HOST, BIND_PORT)
