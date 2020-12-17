import socket
import threading

def start_connection():
    clientSocket = socket.socket()
    clientSocket.connect(('localhost', 8800))
    
    threading._start_new_thread(start_listening, (clientSocket, 1))
    #threading._start_new_thread(send_to_all, (clientSocket, 1))

def start_listening(clientSocket, q):
    while True:
        message = clientSocket.recv(1024).decode()
        print(message)

def send_to_all(clientSocket, q):
    while True:
        message = input(">> ")
        clientSocket.send(message.encode())

if __name__ == "__main__":
    start_connection()