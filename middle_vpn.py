import socket
from udp import receive as udp_receive
from udp import build_packet

TARGET_ADDR = ('127.0.0.3', 8888)
BIND_ADDR = ('127.0.0.100', 9090)

def run_server_vpn():
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    raw_socket.bind(BIND_ADDR)

    print(f"[*] Listening on {BIND_ADDR[0]}:{BIND_ADDR[1]}")

    while True:
        client_addr, request, _ = udp_receive(raw_socket, 1024)

        # Logic for assigning new IP
        new_addr = ('192.168.1.100', 44492)

        print(f"[Client -> Server] {request}")

        packet = build_packet(request, TARGET_ADDR, BIND_ADDR)
        raw_socket.sendto(packet, TARGET_ADDR)


if __name__ == "__main__":
    run_server_vpn()
