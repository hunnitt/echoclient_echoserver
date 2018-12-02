#!/usr/bin/python3

from socket import *
import sys

def usage():
    print("syntax : echoserver <host> <port>")
    print("sample : echoserver 127.0.0.1 1234")
    sys.exit(0)


def main():
    if len(sys.argv) != 3:
        usage()

    host = sys.argv[1]
    port = int(sys.argv[2])

    with socket(AF_INET, SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        while True:
            try:
                msg = input('input message >\n')
                client_socket.sendall(msg.encode())

                response = client_socket.recv(1024).decode()
                print("response from server >")
                print(response + '\n')

            except:
                print("[-] Server ("+sys.argv[1]+":"+sys.argv[2]+") is invalid.")
                print("[-] Connection Refused.")
                sys.exit(1)
        

if __name__ == '__main__':
	main()