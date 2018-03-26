import socket
import threading
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s'
)


def client_handler(sock, address, port):
    while True:
        try:
            message = sock.recv(1024)
            logging.debug(f"Recv: {message} from {address}:{port}")
        except OSError:
            break

        if len(message) == 0:
            break

        sent_message = message
        while True:
            sent_len = sock.send(sent_message)
            if sent_len == len(sent_message):
                break
            sent_message = sent_message[sent_len:]
        logging.debug(f"Send: {message} to {address}:{port}")
    sock.close()
    logging.debug(f"Bye-bye: {address}:{port}")


def main(host: str = 'localhost', port: int = 9090) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    sock.bind((host, port))
    sock.listen(128)
    print(f"Starting TCP Echo Server at {host}:{port}")
    try:
        while True:
            client_sock, (client_addr, client_port) = sock.accept()
            logging.debug(f"New client: {client_addr}:{client_port}")
            client_thread = threading.Thread(
                target=client_handler,
                args=(client_sock, client_addr, client_port))
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        print("Shutting down")
    finally:
        sock.close()


if __name__ == "__main__":
    main()