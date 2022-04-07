import socket
import threading
import time
import sys

# Creates a connection point for later use
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to ip-address from host and opens a port on 2345, which the client can connect to
serverSocket.bind((sys.argv[1], int(sys.argv[2])))

# Allows for one outside connection, that means one connection that is not accepted
serverSocket.listen(1)

# Creates an empty array for storage of clients
clList = []

# Array of names of potential clients
nameArray = ["alice", "brenda", "charlie", "dave", "earl", "felicia", "geir", "homer"]

# Function that interacts with the client, will send an encoded message to the client
# and then call on the function respond
def interact(sendmsg):
    # For-loop iterating through the list on clients
    for i in clList:
        i.send(sendmsg.encode())
    respond()

# Function that sends a message to the client, where the client will send a response
# Function also creates an option to kick out a client if needed through the same input
def rec():
    while True:
        # Lets the server send out a question to the clients
        sendmsg = input("You: ")

        # Converts string to lowercase so that there will be no trouble with the decoding
        sendmsg = sendmsg.lower()

        # Adds "User: " to the front of the string for the display window for the client
        sendmsg = "User: " + sendmsg

        # If-statement that checks if the command /help is written in the input field
        if "/help" in sendmsg:
            print("Use can use /help followed by one the following:")
            print("kick\nverblist\notherwords\nclose")
            # Further checks if the message /help kick is written, so that the correct message is printed
            if "/help kick" in sendmsg:
                print("Syntax: /kick (bot name), bot name must ble lowercase")
                print("Kick closes the connection to the server for the client")
                print("Important note: You have to use correct spelling for the name of the bot")

            # Prints the list of all avaiable verbs
            elif "/help verblist" in sendmsg:
                print("List of useable verbs that the bot will respond to: ")
                print("sing  dance  smile",
                      "\njump  sleep  fight",
                      "\neat  drink  play",
                      "\nfish   work  study",
                      "\nplay  watch  listen",
                      "\nexercise  murder  paint")

            # Lists the remaining commands that the bots will respond to
            elif "/help otherwords" in sendmsg:
                print("List of other useable words that the bot will respond to: ")
                print("feel\nhello\nname")

            elif "/help close" in sendmsg:
                print("Syntax: /close\nCloses the server")

            # If nothing else is specified then the syntax is wrong
            else:
                print("Please use one of the following: ")
                print("kick\nverblist\notherwords")

        # Checks if the command /kick occurs in the input field
        elif "/kick" in sendmsg:
            # Iterates through the array of names to look for the name of the client that should be removed
            for name in nameArray:
                if name in sendmsg:
                    # Creates a variable that carries the name of the client that is going to be kicked
                    client = clList[nameArray.index(name)]
                    # Removes the client from the array of names
                    nameArray.remove(name)
                    # Removes the client for the array of clients
                    clList.remove(client)
                    # Sendes a codeword over to the client so that the connection can ble closed client-side
                    client.send("kicked".encode())
                    print(f"Kicked bot {name} from server")
                    # Closes connection to said client
                    client.close()

        # Creates the ability to close the server through /close
        elif "/close" in sendmsg:
            # Closes the socket
            serverSocket.close()
            # Exits the system
            sys.exit()

        else:
            # If the kick command is not utilized, then the message should be sent to client
            time.sleep(0.1)
            interact(sendmsg)

# Function that recieves a message from client, and sends back the response from clients to other clients
def respond():
    # Iterates through the possible clients that will recieve the message
    for i in clList:
        # Recieves a message that has a capacity of 1024 bits
        recmsg = i.recv(1024).decode()
        if recmsg == "wrong":
            print("Please refer to the list of verbs, /help verblist")
        # Prints the message to server command window
        else:
            print(recmsg)
            for j in clList:
                # If the client "j" is not client "i", then the message will be sent
                # This makes sure that the client can not se its own message
                if j != i:
                    time.sleep(0.1)
                    j.send(recmsg.encode())

# Function that has the purpose of establishing a connection to a client
def connection():
    # Constantly looking for clients
    while True:
        # Accepts clients and gives them a name and an address
        clientSocket, address = serverSocket.accept()
        # Registers the client in the array of clients
        clList.append(clientSocket)
        # Counts the amount of clients, for the purpose of giving the correct alphabetical name to next client
        antall = len(clList)
        # Sends the variable over to the client
        clientSocket.send(str(antall).encode())

def main():
    print(f"Listening for connections...")
    recThread = threading.Thread(target=rec)
    conThread = threading.Thread(target=connection)
    recThread.start()
    conThread.start()

if __name__ == '__main__':
    # Available to be run through the run button in intellij
    main()