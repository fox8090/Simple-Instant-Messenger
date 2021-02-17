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
            if message[5] == 'i':
                user = message[12:]
                allNames[connection] = user
            else:
                user = None
        except:
            connection.send("[SERVER] A valid username is required.").encode()
    helpInfo = "[SERVER] Welcome " + allNames[connection] + "! Type 'quit' to exit. Enjoy!"
    connection.send(helpInfo.encode())
    message = "[SERVER] " + allNames[connection] + " has joined"
    send_to_all(message)
    print(message)
    while True:
        try:
            message = connection.recv(1024).decode()
            if message:
                if message[5] == 'q':
                    allClients[connection].close()
                elif message[5] == 'r':
                    newName = message[12:]
                    message = "[SERVER] " + allNames[connection] + " has changed their name to " + newName + "."
                    allNames[connection] = newName
                    send_to_all(message)
                    print(message)
                elif message[5] == 'u':
                    out = "[SERVER] List of connected users: "
                    for client in allNames:
                        out += allNames[client] + ', '
                    out = out[:len(out)-2] + '.'
                    connection.send(out.encode())
                    print(out)
                elif message[5] == 'w':
                    receiverName = ''
                    toSend = ''
                    space = False
                    for char in message[12:]:
                        if char == ' ' and not space:
                            space = True
                            continue
                        if space:
                            toSend = toSend + char
                        else:
                            receiverName = receiverName + char
                    found = False
                    for client in allNames:
                        if receiverName == allNames[client]:
                            found = True
                            receiver = client
                            break
                    if not found:
                        out = "[SERVER] No such username '" + receiverName + "'. Message not sent."
                        connection.send(out.encode())
                        continue
                    else:
                        out = "[" + allNames[connection] + "] *whispers* " + toSend
                        receiver.send(out.encode())
                        out = "[SERVER] Whisper sent."
                        connection.send(out.encode()) 
                    print(allNames[connection] +" whispers to "+ receiverName + ": " + toSend)

                elif message[5] == 'h':
                    out = "[SERVER] helpful stuff...."
                    connection.send(out.encode())
                    print(out)
                elif message[5] == 'a':
                    out = "[{}] {}".format(allNames[connection], message[12:])
                    send_to_all(out)
                    print(out)
                else:
                    print("ERROR: MESSAGE NOT RECOGNISED")
        except:
            print("[SERVER] Lost connection from", allClients[connection])
            del allClients[connection]
            out = "[SERVER] " + allNames[connection] + " has left."
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