import sys
import socket
import threading

def start_server():
    serverSocket = socket.socket()
    serverSocket.bind(('', int(port)))
    serverSocket.listen(1)
    print("SERVER IS RECEIVING")
    while True:
        connection, clientAddress = serverSocket.accept()
        print("[SERVER] New connection from", clientAddress)
        allClients[connection] = clientAddress
        threading._start_new_thread(new_connection, (connection,))

def new_connection(connection):
    user = None
    while user is None:
        try:
            message = connection.recv(1024).decode()
            if message[5] == 'n':
                user = message[12:]
                allNames[connection] = user
            else:
                user = None
        except:
            connection.send("[SERVER] A valid username is required.")
    helpInfo = "[SERVER] Welcome " + user + "! Type 'quit' to exit. Enjoy!"
    connection.send(helpInfo.encode())
    message = "[SERVER] " + user + " has joined"
    send_to_all(message)
    print(message)
    while True:
        try:
            message = connection.recv(1024).decode()
            if message:
                print(message)
                if message[5] == 'a':
                    print("here")
                    out = "[{}] {}".format(allNames[connection], message[12:])
                    send_to_all(out)
                    print(out)
                else:
                    print("ERROR")
        except:
            print("[SERVER] Lost connection from", allClients[connection])
            del allClients[connection]
            out = "[SERVER] " + allNames[connection] + " has left"
            send_to_all(out)
            print(out)
            del allNames[connection]
            break

def send_to_all(message):
    for client in allClients:
        try:
            client.send(message.encode())
        except:
            closeAll()

def closeAll():
    for client in allClients:
        client.close()
    print("ERROR")
    exit()

if __name__ == "__main__":
    allClients = {}
    allNames ={}
    if len(sys.argv) != 2:
        print("Invalid arguments.\nPlease use the following format: python server.py [port]")
        exit()
    else:
        port = sys.argv[1]
    start_server()