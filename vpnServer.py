import socket
import threading

def handle_client(client_socket, target_host, target_port):
    # Conecta al servidor destino
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_socket.connect((target_host, target_port))

    # Envía datos desde el cliente al servidor destino
    data = client_socket.recv(1024)
    target_socket.send(data)

    # Recibe la respuesta del servidor destino
    target_data = target_socket.recv(1024)
    client_socket.send(target_data)

    # Cierra las conexiones
    target_socket.close()
    client_socket.close()

def run_server_vpn(bind_host, bind_port, target_host, target_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_host, bind_port))
    server.listen(5)

    print(f"[*] Listening on {bind_host}:{bind_port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        client_handler = threading.Thread(
            target=handle_client, args=(client_socket, target_host, target_port)
        )
        client_handler.start()

if __name__ == "__main__":
    BIND_HOST = "127.0.0.1"
    BIND_PORT = 8080
    TARGET_HOST = "127.0.0.1"  # Puedes cambiar esto al IP del servidor destino
    TARGET_PORT = 9090

    run_server_vpn(BIND_HOST, BIND_PORT, TARGET_HOST, TARGET_PORT)
