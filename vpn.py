import socket
import json
import threading
import ipaddress
from unsecure_udp import build_packet, udp_receive
from utils import invalidate_args, validate_input_ip, format_dict, write_log, is_subnet

SERVER_ADDR = ('127.0.0.3', 8888)
BIND_ADDR = ('127.0.0.100', 9090)


class VPN_Server:

    def __init__(self):
        users = 'users.json'
        with open(users, 'r') as users_file:
            self._users = json.load(users_file)
        
        ips = 'ips.json'
        with open(ips, 'r') as ips_file:
            self._ips = json.load(ips_file)

        vlans = 'vlans.json'
        with open(vlans, 'r') as vlans_file:
            self._vlans = json.load(vlans_file)

        restricted_users = 'restricted_users.json'
        with open(restricted_users, 'r') as restricted_users_file:
            self._restricted_users = json.load(restricted_users_file)

        self._threads = []
        self._stop_flag = threading.Event()


    def start_server(self):
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        raw_socket.bind(BIND_ADDR)

        write_log(f"[*] Server started")
        write_log(f'[*] Listening on {BIND_ADDR[0]}: {BIND_ADDR[1]}')

        try:
            while not self._stop_flag.is_set():
                client_addr, request, _ = udp_receive(raw_socket, 1024)

                # Exit in stop case
                if self._stop_flag.is_set():
                    break

                write_log(f'[*] Request: {request}')

                # Analize input
                data = json.loads(request)

                user = data['user']
                password = data['password']
                message = data['message']
                target_addr = (data['target_ip'], int(data['target_port']))

                is_valid = VPN_Server._validate_user(self._users, user, password)
                if is_valid:
                    # Add new thread
                    thread = threading.Thread(target=self._handle_user, args=(raw_socket, user, message, target_addr))
                    self._threads.append(thread)
                    thread.start()

                else:  # Invalid user
                    write_log(f'[*] Invalid user: {user}')
                    continue

        finally:
            # Wait for all threads
            for thread in self._threads:
                thread.join()


    def stop_server(self):
        # Establecer la bandera de detención
        self._stop_flag.set()
        write_log(f"[*] Server stopped")


    def _handle_user(self, raw_socket, user, message, target_addr):
        # Check user restrictions
        if user in self._restricted_users:
            restricted_ips = self._restricted_users[user]

            # Requested ip
            requested_ip = target_addr[0]

            for ip in restricted_ips:
                if is_subnet(requested_ip, ip):
                    # Has no access
                    write_log(f"[*] User: {user} has no access to IP address: {requested_ip}")
                    return


        # Logic for assigning new IP
        new_addr = ('192.168.0.103', 44492)

        write_log(f'[Client -> Server] {message}')

        packet = build_packet(message, target_addr, new_addr)
        raw_socket.sendto(packet, target_addr)

    

    def _create_user(self, username, password, vlan):
        exists = username in self._users
        if exists:
            print("[*] This username already exists")
        else:
            # Update users DB
            self._users[username] = password
            with open('users.json', 'w') as users_file:
                json.dump(self._users, users_file)

            # Generate new ip
            last_ip = list(self._ips.values())[-1]
            ip_obj = ipaddress.ip_address(last_ip)
            new_ip = str(ip_obj + 1)

            # Update ips DB
            self._ips[username] = new_ip
            with open('ips.json', 'w') as ips_file:
                json.dump(self._ips, ips_file)

            # Update vlans DB
            self._vlans[username] = vlan
            with open('vlans.json', 'w') as vlans_file:
                json.dump(self._vlans, vlans_file)

            log =f"[*] User added succesfully\nIP: {new_ip}\nVLAN: {vlan}"
            print(log)
            write_log(log)

    def _restrict_user(self, user, ip):
        # Validate user
        if not user in self._users:
            log = "[*] User does not exist"
            print(log)
            write_log(log)
            return

        if user in self._restricted_users:  # User is restricted
            if not ip in self._restricted_users[user]: # Ip is not restricted
                self._restricted_users[user].append(ip)
        else:
            self._restricted_users[user] = [ip]
        
        log = "[*] User restricted succesfully"
        print(log)
        write_log(log)
        
        # Update DB
        with open('restricted_users.json', 'w') as restricted_users_file:
                json.dump(self._restricted_users, restricted_users_file)
        

    def list_users(self):
        users = format_dict(self._users)
        print(users)
    
    def list_ips(self):
        ips = format_dict(self._ips)
        print(ips)

    def list_vlans(self):
        vlans = format_dict(self._vlans)
        print(vlans)

    def list_users_restrictions(self):
        users_restrictions = format_dict(self._restricted_users)
        print(users_restrictions)

    @staticmethod
    def _validate_user(users, user, password):
        return user in users and users[user] == password




if __name__ == "__main__":
    vpn = VPN_Server()

    while True:
        input_str = input("admin> ")

        splited_input = input_str.split()
        if len(splited_input) == 0:
            print("Invalid input")
            continue

        command = splited_input[0]

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
            # Validate args count
            args = len(splited_input)
            invalid_count = invalidate_args(args-1, 3)
            if not invalid_count:
                continue

            _, username, password, vlan = splited_input

            vpn._create_user(username, password, vlan)

        elif command == "restrict_user":
            # Validate args count
            args = len(splited_input)
            invalid_count = invalidate_args(args-1, 2)
            if invalid_count:
                continue

            _, username, ip = splited_input

            # Validar ip
            valid_ip = validate_input_ip(ip)
            if not valid_ip:
                continue

            vpn._restrict_user(username, ip)
            
        
        elif command == "list_users":
            vpn.list_users()

        elif command == "list_ips":
            vpn.list_ips()

        elif command == "list_vlans":
            vpn.list_vlans()

        elif command == "list_users_restrictions":
            vpn.list_users_restrictions()

        else:
            print("Command not found")

