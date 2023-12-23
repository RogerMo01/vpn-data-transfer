import socket
import json
import threading
import ipaddress
# from udp import receive as udp_receive
# from udp import build_packet
from unsecure_udp import build_packet
from unsecure_udp import udp_receive

TARGET_ADDR = ('127.0.0.3', 8888)
BIND_ADDR = ('127.0.0.100', 9090)

class VPN_Server:

    def __init__(self):
        users = 'users.json'
        with open(users, 'r') as ips_file:
            self._users = json.load(ips_file)
        
        ips = 'ips.json'
        with open(ips, 'r') as ips_file:
            self._ips = json.load(ips_file)

        self._threads = []
        self._stop_flag = threading.Event()


    def start_server(self):
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        raw_socket.bind(BIND_ADDR)

        print(f"[*] Listening on {BIND_ADDR[0]}:{BIND_ADDR[1]}")

        try:
            while not self._stop_flag.is_set():
                client_addr, request, _ = udp_receive(raw_socket, 1024)

                # Exit in stop case
                if self._stop_flag.is_set():
                    break

                print(f"[*] Request: {request}")
                # Analize input
                data = json.loads(request)

                user = data['user']
                password = data['password']
                message = data['message']

                is_valid = VPN_Server._validate_user(self._users, user, password)
                if is_valid:
                    print(f"[*] Valid user: {user}")

                    # Add new thread
                    thread = threading.Thread(target=self._handle_user, args=(raw_socket, message))
                    self._threads.append(thread)
                    thread.start()
                    
                else: #Invalid user
                    print(f"[*] Invalid user: {user}")
                    continue

        finally:
            # Wait for all threads
            for thread in self._threads:
                thread.join()

    def stop_server(self):
        # Establecer la bandera de detención
        self._stop_flag.set()
            
    
    def _handle_user(self, raw_socket, message):
        # Logic for assigning new IP
        new_addr = ('192.168.0.103', 44492)

        print(f"[Client -> Server] {message}")

        packet = build_packet(message, TARGET_ADDR, new_addr)
        raw_socket.sendto(packet, TARGET_ADDR)

    def _create_user(self, username, password):
        exists = username in self._users
        if exists:
            print("[*] This username already exists")
        else:
            # Update users DB
            self._users[username] = password
            with open('users.json', 'w') as ips_file:
                json.dump(self._users, ips_file)

            # Generate new ip
            last_ip = list(self._ips.values())[-1]
            ip_obj = ipaddress.ip_address(last_ip)
            new_ip = str(ip_obj + 1)

            # Update ips DB
            self._ips[username] = new_ip
            with open('ips.json', 'w') as ips_file:
                json.dump(self._ips, ips_file)
                
            print(f"[*] User added succesfully with IP: {new_ip}")


    @staticmethod
    def _validate_user(users, user, password):
        return user in users and users[user] == password
            



if __name__ == "__main__":
    vpn = VPN_Server()

    while True:
        command = input("command> ")

        if command == "exit":
            vpn.stop_server()
            break
        elif command == "start":
            vpn._stop_flag.clear()

            server_thread = threading.Thread(target=vpn.start_server)
            server_thread.start()

        elif command == "stop":
            vpn.stop_server()
        elif command == "create_user":
            username = input("Enter username: ")
            password = input("Enter password: ")
            vpn._create_user(username, password)
        else:
            print("Command not found")
        

