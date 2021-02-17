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
    clientSocket.send(("type:i data:" + username).encode())
    while True:
        message = input()
        if message == 'quit':
            clientSocket.send(("type:q data:None").encode())
            clientSocket.close()
            break
        elif message[:7] == 'rename ':
            clientSocket.send(("type:r data:" + message[8:]).encode())
        elif message == 'users':
            clientSocket.send(("type:u data:None").encode())
        elif message[:8] == 'whisper ':
            clientSocket.send(("type:w data:" + message[9:]).encode())
        elif message == 'help':
            clientSocket.send(("type:h data:None").encode())
        else:
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