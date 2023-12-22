import socket
from udp import receive as udp_receive
from udp import build_packet

def handle_client(request, new_addr, target_host, target_port):
    print(f"[Client -> Server] {request}")

    

def run_server_vpn(bind_host, bind_port, target_host, target_port):
    vpn_addr = (bind_host, bind_port)
    server_addr = (target_host, target_port)

    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    recv_socket.bind(vpn_addr)

    print(f"[*] Listening on {bind_host}:{bind_port}")


    while True:
        client_addr, request, _ = udp_receive(recv_socket, 1024)
        new_addr = ('192.168.1.100', 44492)

        print(f"[Client -> Server][{new_addr} -> {server_addr}] {request}")
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        
        print(raw_socket)

        packet = build_packet(request, server_addr, new_addr)

        print("paquete")
        print(packet)

        raw_socket.sendto(packet, server_addr)

        print(f"se debe haber mandado {packet} a {server_addr}")

        # Inicia un hilo para manejar la conexión del cliente
        # client_handler = threading.Thread(target=handle_client, args=(request, new_addr, target_host, target_port))
        # client_handler.start()



if __name__ == "__main__":
    BIND_HOST = "127.0.0.2"
    BIND_PORT = 9090

    TARGET_HOST = "127.0.0.3"
    TARGET_PORT = 8888

    run_server_vpn(BIND_HOST, BIND_PORT, TARGET_HOST, TARGET_PORT)
