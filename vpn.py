import socket
import json
import threading
# from udp import receive as udp_receive
# from udp import build_packet
from unsecure_udp import build_packet
from unsecure_udp import udp_receive

TARGET_ADDR = ('127.0.0.3', 8888)
BIND_ADDR = ('127.0.0.100', 9090)

class VPN_Server:
    

    def __init__(self):
        self._users = {'Pedro': 'picapiedra'}
        self._ips = {'Pedro': '192.168.1.1'}
        self._threads = []

    def start(self):
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        raw_socket.bind(BIND_ADDR)

        print(f"[*] Listening on {BIND_ADDR[0]}:{BIND_ADDR[1]}")

        try:
            while True:
                client_addr, request, _ = udp_receive(raw_socket, 1024)

                print(f"[*] Request: {request}")
                # Analize input
                data = json.loads(request)

                user = data['user']
                password = data['password']
                message = data['message']

                is_valid = VPN_Server._validate_user(self._users, user, password)
                if is_valid:
                    print(f"[*] Valid user: {user}")

                    # Crear un hilo para manejar la conexión del usuario
                    thread = threading.Thread(target=self._handle_user, args=(raw_socket, message))
                    self._threads.append(thread)
                    thread.start()
                    
                else: #Invalid user
                    print(f"[*] Invalid user: {user}")
                    continue

                # Break snippet
                if(message == 'break'): 
                    break
        finally:
            # Wait for all threads
            for thread in self._threads:
                thread.join()


            
    
    def _handle_user(self, raw_socket, message):
        # Logic for assigning new IP
        new_addr = ('192.168.0.103', 44492)

        print(f"[Client -> Server] {message}")

        packet = build_packet(message, TARGET_ADDR, new_addr)
        raw_socket.sendto(packet, TARGET_ADDR)

        
        

    @staticmethod
    def _validate_user(users, user, password):
        return user in users and users[user] == password
            



if __name__ == "__main__":
    vpn = VPN_Server()

    vpn.start()

