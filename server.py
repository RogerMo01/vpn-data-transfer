import socket

def square(n):
    return n*n

def run_server(bind_host, bind_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_host, bind_port))
    server.listen(5)

    print(f"[*] Listening on {bind_host}:{bind_port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")


        # Process request
        data = client_socket.recv(1024)
        decoded_data = data.decode('utf-8')
        print(f"[*] Received number: {decoded_data}")

        try:
            n = int(decoded_data)
            response = f"{square(n)}"
        except ValueError:
            response = "Error: La cadena no es un número entero válido."

        client_socket.send(response.encode("utf-8"))


        # Cierra la conexión
        client_socket.close()

if __name__ == "__main__":
    BIND_HOST = "127.0.0.1"
    BIND_PORT = 9090

    run_server(BIND_HOST, BIND_PORT)
