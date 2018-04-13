#Однопоточный вебсервер

import socket
import time


def main(host: str = 'localhost', port: int = 9090) -> None:
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    serversocket.bind((host, port))
    serversocket.listen(128)

    print(f"Starting Web Server at {host}:{port}")
    try:
        while True:
            clientsocket, (client_addr, client_port) = serversocket.accept()
            print(f"Принял клиента: {client_addr, client_port}")
            data = clientsocket.recv(1024)
            time.sleep(0.3)
            clientsocket.sendall(
                b"HTTP/1.1 200 OK\r\n"
                b"Content-Type: text/html\r\n"
                b"Content-Length: 71\r\n\r\n"
                b"<html><head><title>Success</title></head><body>" + b"your ip: " +client_addr.encode() + b"</body></html>"
            )
            print(data)
            clientsocket.close()
    except KeyboardInterrupt:
        print("Shutting down")
    finally:
        serversocket.close()

if __name__ == "__main__":
    main()
