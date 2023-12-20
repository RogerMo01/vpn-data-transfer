import socket
from udp import recive as udp_recive

def square(n):
    return n*n

def run_server(bind_host, bind_port):
    server_addr = (bind_host, bind_port)

    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP) as s:
        s.bind(server_addr)

        print(f"[*] Listening on {bind_host}:{bind_port}")

        while True:
            request, valid = udp_recive(s, 1024)
            
            response = ""
            if(not valid):
                response = request
            else:
                # Process request
                print(f"[<] Process : {request}")
                try:
                    n = int(request)
                    response = f"{square(n)}"
                except ValueError:
                    response = "Error(La cadena no es un número entero válido)"

            print(f"[>] Response: {response}")

if __name__ == "__main__":
    BIND_HOST = "127.0.0.1"
    BIND_PORT = 9090

    run_server(BIND_HOST, BIND_PORT)
