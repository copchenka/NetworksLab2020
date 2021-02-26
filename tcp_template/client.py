from socket import *
import sys
import threading

HOST = '127.0.0.1'
PORT = 8080
HEADER_SIZE = 10
TIME = 10
FORMAT = 'utf-8'


def _send():
    while True:

        msg = input()
        try:
            if msg == "-exit":
                msg = f"Пользователь {nickname.decode(FORMAT)} вышел из чата"
                msg = msg.encode(FORMAT)
                msg_header = f"{len(msg):<{HEADER_SIZE}}".encode(FORMAT)
                sock.send(msg_header + msg)
                sock.shutdown(SHUT_RDWR)
                sock.close()
                sys.exit(0)
        except OSError:
            print('Сервер завершил соединение')
            exit(0)

        if msg:
            msg = msg.encode(FORMAT)
            msg_header = f"{len(msg):<{HEADER_SIZE}}".encode(FORMAT)
            sock.send(msg_header + msg)


def _receive():
    while True:
        try:
            username_header = sock.recv(HEADER_SIZE)
            if not len(username_header):
                print("Connection closed by server")
                exit(0)

            username_length = int(username_header.decode(FORMAT))
            username = sock.recv(username_length).decode(FORMAT)

            message_header = sock.recv(HEADER_SIZE)
            message_length = int(message_header.decode(FORMAT))

            message = sock.recv(message_length).decode(FORMAT)

            time = sock.recv(TIME).decode(FORMAT)

            print(f'<{time}> [{username}]: {message}')
        except OSError:
            exit(0)

        except Exception as e:
            print('Error', str(e))
            exit(0)


sock = socket(AF_INET, SOCK_STREAM)
sock.connect((HOST, PORT))

nickname = input("Username: ").encode(FORMAT)
username_header = f"{len(nickname):<{HEADER_SIZE}}".encode(FORMAT)

sock.send(username_header + nickname)
send_thread = threading.Thread(target=_send).start()
receive_thread = threading.Thread(target=_receive).start()
