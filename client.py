import socket

def run_client(target_host, target_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host, target_port))

    # Envia datos al servidor VPN
    message = "Hola desde el cliente"
    client.send(message.encode("utf-8"))

    # Recibe la respuesta del servidor VPN
    response = client.recv(1024)
    print(f"[*] Received from VPN: {response.decode('utf-8')}")

    # Cierra la conexión
    client.close()

if __name__ == "__main__":
    TARGET_HOST = "127.0.0.1"
    TARGET_PORT = 8080

    run_client(TARGET_HOST, TARGET_PORT)
