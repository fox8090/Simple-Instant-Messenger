import sys
import socket
import threading
import logging

def start_server():
    serverSocket = socket.socket()
    serverSocket.bind(('', int(port)))
    serverSocket.listen(1)
    print("Server starting.")
    while True:
        connection, clientAddress = serverSocket.accept()
        logging.info("Established new connection from %s.", clientAddress)
        print("[SERVER] New connection from", clientAddress)
        allClients[connection] = clientAddress
        threading._start_new_thread(new_connection, (connection, clientAddress))

def new_connection(connection, clientAddress):
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
            logging.warning("User %s has entered an invalid username.", allClients[connection])
            connection.send("[SERVER] A valid username is required.").encode()
            logging.info("[SERVER] -> [%s] A valid username is required.", allClients[connection])
    helpInfo = "[SERVER] Welcome " + allNames[connection] + "! Type 'help' for commands. Enjoy!"
    connection.send(helpInfo.encode())
    logging.info("[SERVER] -> [%s] Welcome %s! Type 'help' for commands. Enjoy!", allNames[connection], allNames[connection])
    message = "[SERVER] " + allNames[connection] + " has joined."
    send_to_all(message)
    logging.info("[SERVER] -> [ALL] %s has joined.", allNames[connection])
    print(message)
    while True:
        try:
            message = connection.recv(1024).decode()
            if message:
                print(message)
                if message[5] == 'q':
                    logging.info("User at %s requested to close connection.")
                    connection.close()
                    logging.info("Connection at %s has been closed.", clientAddress)
                elif message[5] == 'r':
                    newName = message[12:]
                    message = "[SERVER] " + allNames[connection] + " has changed their name to " + newName + "."
                    
                    logging.info("Changed username for %s to %s.", clientAddress, newName)
                    send_to_all(message)
                    logging.info("[SERVER] -> [ALL] %s has changed their name to %s.", allNames[connection], newName)
                    print(message)
                    allNames[connection] = newName
                elif message[5] == 'u':
                    logging.info("User at %s requested a list of users.", clientAddress)
                    out = "[SERVER] List of connected users: "
                    for client in allNames:
                        out += allNames[client] + ', '
                    out = out[:len(out)-2] + '.'
                    connection.send(out.encode())
                    logging.info("[SERVER] -> [%s] %s,", allNames[connection], out[9:])
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
                        logging.warning("User at %s attempted to whisper to a user that doesn't exist.", clientAddress)
                        logging.info("[SERVER] -> [%s] No such username '%s'. Message not sent.", allNames[connection], receiverName)
                        continue
                    else:
                        out = "[" + allNames[connection] + "] *whispers* " + toSend
                        receiver.send(out.encode())
                        logging.info("[%s] -> [%s] *whispers* %s", allNames[connection], receiverName, toSend)
                        out = "[SERVER] Whisper sent."
                        connection.send(out.encode()) 
                        logging.info("[SERVER] -> [%s] Whisper sent.", allNames[connection])
                    print(allNames[connection] +" whispers to "+ receiverName + ": " + toSend)

                elif message[5] == 'h':
                    logging.info("User at %s requested list of help commands.", clientAddress)
                    out = "[SERVER] You can type messages and press enter to send. Or you can use the following commands:\n         quit -> exits program\n         users -> displays list of connected users\n         rename newname -> changes your username to newname\n         whisper user message -> sends user a message only\n         help -> displays this help message"
                    connection.send(out.encode())
                    logging.info("[SERVER] - [%s] %s", allNames[connection], out[9:])
                    print(out)
                elif message[5] == 'a':
                    out = "[{}] {}".format(allNames[connection], message[12:])
                    for client in allClients:
                        if connection != client:
                            try:
                                client.send(out.encode())
                            except:
                                closeAll
                    print(out)
                    logging.info("[SERVER] -> [ALL] %s", message[12:])
                else:
                    logging.error("Message from client at %s not recognised.", clientAddress)
                    print("ERROR: MESSAGE NOT RECOGNISED")
        except:
            print("[SERVER] Lost connection from", clientAddress)
            logging.warning("Lost connection from %s", clientAddress)
            del allClients[connection]
            out = "[SERVER] " + allNames[connection] + " has left."
            send_to_all(out)
            logging.info("[SERVER] -> [ALL] %s has left.", allNames[connection])
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
    logging.critical("All connections closed. Server stopped.")
    exit()

if __name__ == "__main__":
    allClients = {}
    allNames ={}
    if len(sys.argv) != 2:
        print("Invalid arguments.\nPlease use the following format: python server.py [port]")
        exit()
    else:
        port = sys.argv[1]
        logging.basicConfig(filename="server.log", level=logging.INFO, format="%(asctime)s - %(levelname)s :  %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
        logging.info("Server started.")
    start_server()