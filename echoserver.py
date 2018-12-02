#!/usr/bin/python3

from socket import *
from threading import *
import sys

client_sockets = []
lock = Lock()

def usage():
    print("syntax : echoserver <port> [-b]")
    print("sample : echoserver 1234 -b")
    sys.exit(0)

def echo2cli(client_socket, is_b):
    while True:
        msg = client_socket.recv(1024).decode()
        if msg == 0:
            with lock:
                print("[-] Client disconnected!")
                client_sockets.remove()
                print("[-] ",len(client_sockets)," clients left.")
                client_socket.close()
                break
            
        elif is_b:
            print(msg,'\n')
            with lock:
                for cli_sock in client_sockets:
                    cli_sock.send(msg.encode())

        elif not is_b:
            with lock:
                client_socket.send(msg.encode())

def server(server_socket, is_b):
    print("[+] Waiting for clients...\n")
    
    try:
        while True:
            client_socket, client_addr = server_socket.accept()
            with lock:
                client_sockets.append(client_socket)
            print("[+] New Connection from",client_addr,"!\n")
            new_client = Thread(target=echo2cli, args=(client_socket, is_b))
            new_client.start()

    except KeyboardInterrupt:
        print("[-] Keyboard Interrupt")
        print("[-] Server Closed")
        new_client.join()
        sys.exit(1)

def main():
    if len(sys.argv) != 3 and len(sys.argv) != 2:
        usage()
    elif len(sys.argv) == 3 and sys.argv[2] == '-b':
        is_b = True
    else:
        is_b = False

    port = int(sys.argv[1])
    server_socket = socket(AF_INET , SOCK_STREAM)
    server_socket.bind(('127.0.0.1', port))
    server_socket.listen(20)

    server(server_socket, is_b)

    
if __name__ == '__main__':
	main()