import socket

def run_server(bind_host, bind_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_host, bind_port))
    server.listen(5)

    print(f"[*] Listening on {bind_host}:{bind_port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        data = client_socket.recv(1024)
        print(f"[*] Received data: {data.decode('utf-8')}")

        # Simula el procesamiento y generación de respuesta
        response = "Hola desde el servidor destino"
        client_socket.send(response.encode("utf-8"))

        # Cierra la conexión
        client_socket.close()

if __name__ == "__main__":
    BIND_HOST = "127.0.0.1"
    BIND_PORT = 9090

    run_server(BIND_HOST, BIND_PORT)
