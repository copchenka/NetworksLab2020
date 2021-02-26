import time
from socket import *
import threading

HOST = '127.0.0.1'
PORT = 8080
HEADER_SIZE = 10
FORMAT = 'utf-8'
clients = {}


def send(s_client, u_name):
    while True:
        msg = receive(s_client)
        try:
            if msg is False:
                close(s_client)
                continue
        except:
            continue

        message_time = time.strftime("%H:%M:%S", time.localtime()).encode(FORMAT)
        print(
            f"Received message from {u_name['data'].decode(FORMAT)} at {message_time.decode(FORMAT)}: {msg['data'].decode(FORMAT)}")

        for client in clients:
            if client != s_client:
                client.send(u_name['header'] + u_name['data'] + msg['header'] + msg['data'] + message_time)


def receive(s_client):
    while True:
        try:
            message_header = s_client.recv(HEADER_SIZE)
            if not len(message_header):
                return False
            message_length = int(message_header.decode(FORMAT).strip())
            return {"header": message_header, "data": s_client.recv(message_length)}
        except:
            return False


def close(s_client):
    cl = clients[s_client]['data'].decode(FORMAT)
    s_client.close()
    del clients[s_client]
    print(f'Client {cl} disconnected')


def main():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(10)
    while True:
        s_client, addr = sock.accept()
        u_name = receive(s_client)
        print(f"Запрос на соединение от {s_client}" f"Username: {u_name['data'].decode(FORMAT)}")
        clients[s_client] = u_name
        threading.Thread(target=send, args=(s_client, u_name,)).start()


if __name__ == '__main__':
    main()
