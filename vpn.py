import socket
import json
import threading
# from udp import receive as udp_receive
# from udp import build_packet
from unsecure_udp import build_packet
from unsecure_udp import udp_receive
from datetime import datetime

TARGET_ADDR = ('127.0.0.3', 8888)
BIND_ADDR = ('127.0.0.100', 9090)


class VPN_Server:

    def __init__(self):
        self._users = {'Pedro': 'picapiedra'}
        self._ips = {'Pedro': '192.168.1.1'}
        self._threads = []
        self._stop_flag = threading.Event()


    def start_server(self):
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        raw_socket.bind(BIND_ADDR)

        log = ''

        log = f'[*] Listening on {BIND_ADDR[0]}: {BIND_ADDR[1]}'
        write_logs(log)

        try:
            while not self._stop_flag.is_set():
                client_addr, request, _ = udp_receive(raw_socket, 1024)

                # Exit in stop case
                if self._stop_flag.is_set():
                    break

                log = f'[*] Request: {request}'
                write_logs(log)

                # Analize input
                data = json.loads(request)

                user = data['user']
                password = data['password']
                message = data['message']

                is_valid = VPN_Server._validate_user(self._users, user, password)
                if is_valid:
                    log = f'[*] Valid user: {user}'
                    write_logs(log)

                    # Add new thread
                    thread = threading.Thread(target=self._handle_user, args=(raw_socket, message))
                    self._threads.append(thread)
                    thread.start()

                else:  # Invalid user
                    log = f'[*] Invalid user: {user}'
                    write_logs(log)
                    continue

                # Break snippet
                if (message == 'break'):
                    break
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

        log = f'[Client -> Server] {message}'
        write_logs(log)

        packet = build_packet(message, TARGET_ADDR, new_addr)
        raw_socket.sendto(packet, TARGET_ADDR)


    @staticmethod
    def _validate_user(users, user, password):
        return user in users and users[user] == password


def write_logs(log):
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open('logs.txt', 'a') as file:
        file.write(date_time + ': ' + log + '\n')


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
        else:
            print("Command not found")
