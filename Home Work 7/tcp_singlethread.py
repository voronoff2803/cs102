import socket

def main(host: str = 'localhost', port: int = 9090) -> None:
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    serversocket.bind((host, port))
    serversocket.listen(5)

    print(f"Starting Echo Server at {host}:{port}")
    try:
        while True:
            clientsocket, (client_address, client_port) = serversocket.accept()
            print(f"New client {client_address}:{client_port}")

            while True:
                try:
                    data = clientsocket.recv(1024)
                    print(f"Recv: {data}")
                except OSError:
                    break

                if not len(data):
                    break

                sent_data = data
                while True:
                    sent_len = clientsocket.send(sent_data)
                    if sent_len == len(data):
                        break
                    sent_data = sent_data[sent_len:]
                print(f"Send: {data}")

            clientsocket.close()
            print(f"Bye-bye: {client_address}:{client_port}")
    except KeyboardInterrupt:
        print("Shutting down")
    finally:
        serversocket.close()

if __name__ == "__main__":
    main()