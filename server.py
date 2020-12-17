import socket
import threading

def start_server():
    serverSocket = socket.socket()
    serverSocket.bind(('', 8800))
    serverSocket.listen()
    print("SERVER IS RECEIVING")
    while True:
        connection, clientAddress = serverSocket.accept()
        print("join from ", clientAddress)
        welcomeMessage = "welcome enter name"
        connection.send(welcomeMessage.encode())
        allClients[connection] = clientAddress
        threading._start_new_thread(new_connection, (connection, clientAddress))

def new_connection(connection, clientAddress):
    user = connection.recv(1024).decode()
    helpInfo = "Welcome " + user + ", heres how to use"
    connection.send(helpInfo.encode())
    message = user + "has joined"
    send_to_all(message)
    while True:
        message = connection.recv(1024).decode()
        send_to_all(message)
        print("{}: {}".format(clientAddress, message))

def send_to_all(message):
    for client in allClients:
        client.send(message.encode())

if __name__ == "__main__":
    allClients = {}
    start_server()