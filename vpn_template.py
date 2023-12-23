import socket
import threading
from udp import receive as udp_receive
from udp import build_packet

VPN_ADDR = ('127.0.0.100', 9090)

# Servers
SERVER1_ADDR = ('127.0.0.3', 8888)


class VPN_Server:

    def __init__(self, use_udp):
        self.protocol_type = use_udp
        # Diccionario para almacenar información de los usuarios (contraseña, nombre, dirección IP asignada)
        self.users = {'user': 'password'}
        self.vlan_restrictions = {}  # Almacenar restricciones de acceso por VLAN
        self.user_restrictions = {}  # Almacenar restricciones de acceso por usuario
        # Crear un socket raw
        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        # # Configurar el socket para recibir todos los paquetes UDP
        # self.socket.bind(("0.0.0.0", 8888))

    def start(self):
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        raw_socket.bind(VPN_ADDR)

        print(f"VPN Server started on {VPN_ADDR[0]}:{VPN_ADDR[1]}, Esperando conexiones...")

        while True:
            client_addr, request, _ = udp_receive(raw_socket, 1024)

            # Logic for assigning new IP
            new_addr = ('192.168.1.100', 44492)

            print(f"[Client -> Server] {request}")

            packet = build_packet(request, SERVER1_ADDR, VPN_ADDR)
            raw_socket.sendto(packet, SERVER1_ADDR)



    def receive_packets(self):

        while True:
            raw_data, addr = self.server_socket.recvfrom(65536)
            self.process_udp_packet(raw_data, addr)

    def process_udp_packet(self, raw_data, addr):
        # Implementar la lógica para procesar el paquete UDP según tus requisitos
        pass

    def stop(self):
        # Implementar la lógica para detener el servidor VPN
        pass

    def create_user(self, name, password, id_vlan):
        # Implementar la lógica para crear un nuevo usuario y asignar una IP virtual
        pass

    def restrict_vlan(self, id_vlan, ip_network):
        # Implementar la lógica para restringir el acceso a un rango de IP por VLAN
        pass

    def restrict_user(self, id_user, ip_network):
        # Implementar la lógica para restringir el acceso a una red específica por usuario
        pass

    def handle_client(self, client_socket, address):
        # Implementar la lógica para manejar la comunicación con el cliente
        pass

    def log_traffic(self, log_entry):
        # Implementar la lógica para registrar el tráfico y los pedidos rechazados
        pass


# Ejemplo de uso
if __name__ == "__main__":
    protocol_type = "use_udp"
    vpn_server = VPN_Server(protocol_type)

    vpn_server.start()



    # # Hilo para manejar la entrada del usuario desde el terminal
    # user_input_thread = threading.Thread(target=vpn_server.start)
    # user_input_thread.start()

    # # Implementar la lógica para aceptar conexiones de clientes y manejar cada conexión en un hilo separado
    # while True:
    #     client_socket, client_address = vpn_server.accept_client()
    #     client_thread = threading.Thread(
    #         target=vpn_server.handle_client, args=(client_socket, client_address))
    #     client_thread.start()
