import socket
# from udp import receive as udp_receive
# from udp import build_packet
from unsecure_udp import build_packet
from unsecure_udp import udp_receive

TARGET_ADDR = ('127.0.0.3', 8888)
BIND_ADDR = ('127.0.0.100', 9090)

class VPN_Server:
    def __init__(self):
        pass

    def start(self):
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        raw_socket.bind(BIND_ADDR)

        print(f"[*] Listening on {BIND_ADDR[0]}:{BIND_ADDR[1]}")

        while True:
            client_addr, request, _ = udp_receive(raw_socket, 1024)

            # Logic for assigning new IP
            new_addr = ('192.168.0.103', 44492)

            print(f"[Client -> Server] {request}")

            packet = build_packet(request, TARGET_ADDR, new_addr)
            
            raw_socket.sendto(packet, TARGET_ADDR)





if __name__ == "__main__":
    vpn = VPN_Server()

    vpn.start()

