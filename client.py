import socket

def run_client(target_host, target_port):
    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target_host, target_port))

        # Envia datos al servidor VPN
        message = input()
        
        if(message == 'exit'): 
            # client.close()
            break

        client.send(message.encode("utf-8"))

        # Recibe la respuesta del servidor VPN
        response = client.recv(1024)
        print(f"[*] Received response: {response.decode('utf-8')}")

        # Cierra la conexión
        client.close()

if __name__ == "__main__":
    TARGET_HOST = "127.0.0.1"
    TARGET_PORT = 8080

    run_client(TARGET_HOST, TARGET_PORT)
