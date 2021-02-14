import sys
import socket
import threading
import time

'''python server.py [port]python client.py [username] [hostname] [port'''

def start_connection():
    clientSocket = socket.socket()
    try:
        clientSocket.connect((hostname, int(port)))
    except:
        print("Server is not available or port/hostname are wrong.")
        exit()

    threading.Thread(target=receiver, args=(clientSocket, )).start()
    threading.Thread(target=sender, args=(clientSocket, )).start()
    

def sender(clientSocket):
    clientSocket.send(("type:n data:" + username).encode())
    while True:
        message = input()
        if message == 'quit':
            clientSocket.close()
            break
        clientSocket.send(("type:a data:"+message).encode())
        

def receiver(clientSocket):
    while True:
        try:
            received = clientSocket.recv(1024)
            if received:
                print("\r" + received.decode() + "\n>> ", end="")
        except:
            exit()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Invalid arguments.\nPlease use the following format: python client.py [username] [hostname] [port]\n")
        exit()
    else:
        username = sys.argv[1]
        hostname = sys.argv[2]
        port = sys.argv[3]
        start_connection()