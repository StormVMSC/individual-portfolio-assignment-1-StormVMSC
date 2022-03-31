import socket
import sys
import random

# Creates a connection point for later use
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connects the client to the server of given ip and port
clientSocket.connect((sys.argv[1], int(sys.argv[2])))

# Recieves the variable that counts the total amount of clients
teller = clientSocket.recv(1024).decode()

# Arrays containing usable verbs, moods and names
wordArray = ["sing", "dance", "smile", "jump", "sleep", "fight", "eat",
             "drink", "play", "fish", "work" , "study", "play", "watch",
             "listen", "exercise", "murder", "paint", "feel", "hello", "name"]
moodArray = ["angry", "happy", "sad", "neutral", "hungry", "stressed"]
nameArray = ["Alice", "Benny", "Charlie", "Dave", "Earl", "Felicia", "Geir", "Homer"]

# Function that decodes a message and detects the verb and name in a sentence
def decoder(msg):
    # Empty strings that will be overwritten
    acting = ""
    name = ""

    # For-loop that iterates through the word list and detects if the word is in it
    for act in wordArray:
        if act in msg:
            # Storage variable that keeps the verb availble for use in bot-response
            acting = act

    # For-loop that iterates through the name list and detects which name is on the message
    for na in nameArray:
        if na in msg:
            # Stores the name messenger in a variable, so that it can be used to not show the clients own messages
            name = na

    # Returns both storage variables
    return acting, name

# The function that established a randomized bot based on mood given at random when connecting to the server
def bot(name, mood):
    print(f"Welcome, {nameArray[int(teller)-1]}")
    # While-loop so that the bot can respond multiple times to questions from the server
    while True:
        # Creates a variable that stores the decoded message from the server
        msg = clientSocket.recv(1024).decode()

        # Checks if the codeword kicked is in the message
        if msg == "kicked":
            # Closes the connection from the client
            clientSocket.close()
        # Creates two variables that takes the verb and the name from the message
        act, na = decoder(msg)
        # The variable name will match with one from the name list, -1 makes sure that it is the correct name
        name = nameArray[int(teller)-1]
        # Shows the message
        print(msg)

        # Checks in the name of the sender of said message is the same as the current running client
        if na in nameArray:
            # The client will skip over the response stage if it is its own message
            continue

        # The text-lines for the bots to use depending on mood
        else:
            # Generates a random number between 0 and 5 to randomize response
            randomInt = random.randint(0,5)
            # Checks if the user has typed in a useable word
            if act not in wordArray:
                # Sends codeword "wrong" to the server in order to direct user attention to the given list of words
                clientSocket.send("wrong".encode())

            else:
                if act == "feel":
                    clientSocket.send(f"{name}: I feel {mood}".encode())
                elif act == "hello":
                    clientSocket.send(f"{name}: Hello!".encode())
                elif act == "name":
                    clientSocket.send(f"{name}: My name is {name}".encode())

                else:
                    if mood == "angry":
                        if act == "fight":
                            if randomInt >= 2:
                                # Sends a message to the server containing the name of the bot and a text line based upon the given verb
                                clientSocket.send(f"{name}: A {act}? A worthy opponent! Our battle will be legendary".encode())
                            else:
                                clientSocket.send(f"{name}: I agree to partake in combat".encode())
                        elif act == "murder":
                            if randomInt == 5:
                                clientSocket.send(f"{name}: Tonight is the night..".encode())
                            else:
                                clientSocket.send(f"{name}: I wouldn't go that far".encode())
                        else:
                            if randomInt >= 2:
                                clientSocket.send(f"{name}: I don't like that idea, can we do anything else than {act}?".encode())
                            else:
                                clientSocket.send(f"{name}: Sounds stupid, I would rather fight..".encode())

                    elif mood == "happy":
                        if act == "fight" or act == "sleep" or act == "work" or act == "study":
                            if randomInt >= 2:
                                clientSocket.send(f"{name}: We can {act}, i'm fine with that".encode())
                            else:
                                clientSocket.send(f"{name}: I'm not so sure, doesn't sound that appealing".encode())
                        elif act == "murder":
                            if randomInt == 5:
                                clientSocket.send(f"{name}: Oh the horror".encode())
                            else:
                                clientSocket.send(f"{name}: Why did you suggest that?".encode())
                        else:
                            if randomInt >= 2:
                                clientSocket.send(f"{name}: Good idea! I think {act}ing is fun".encode())
                            else:
                                clientSocket.send(f"{name}: Yes! we should be {act}ing".encode())

                    elif mood == "sad":
                        if act == "sleep" or act == "eat":
                            if randomInt >= 2:
                                clientSocket.send(f"{name}: I guess {act}ing is fine".encode())
                            else:
                                clientSocket.send(f"{name}: Alright, if I must".encode())

                        elif act == "murder":
                            if randomInt == 5:
                                clientSocket.send(f"{name}: I really couldn't care less if I die".encode())
                            else:
                                clientSocket.send(f"{name}: Really..".encode())
                        else:
                            if randomInt >= 1:
                                clientSocket.send(f"{name}: Can't we do something else please?".encode())
                            else:
                                clientSocket.send(f"{name}: Through me you go into a city of weeping; through me you go into eternal"
                                                  f" pain; through me you go amongst the lost people.".encode())

                    elif mood == "neutral":
                        if act == "murder":
                            if randomInt == 5:
                                clientSocket.send(f"{name}: Please no!".encode())
                            else:
                                clientSocket.send(f"{name}: Stupid suggestion".encode())
                        elif randomInt == 0:
                            clientSocket.send(f"{name}: {act}ing? Why not?".encode())
                        elif randomInt == 1:
                            clientSocket.send(f"{name}: Fine by me".encode())
                        elif randomInt == 2:
                            clientSocket.send(f"{name}: I think {act}ing is okay".encode())
                        else:
                            clientSocket.send(f"{name}: Yeah, {act}ing is doable".encode())

                    elif mood == "hungry":
                        if act == "eat":
                            clientSocket.send(f"{name}: Finally, i'm starving".encode())
                        elif act == "murder":
                            clientSocket.send(f"{name}: Waste of time if you ask me".encode())
                        else:
                            clientSocket.send(f"{name}: I'm so hungry, shouldn't we rather eat?".encode())

                    elif mood == "stressed":
                        if act == "work" or act == "study" or act == "code":
                            if randomInt > 3:
                                clientSocket.send(f"{name}: Good idea, we should stop procrastinating. About time for some {act}ing".encode())
                            else:
                                clientSocket.send(f"{name}: Excellent choice, we need to {act}".encode())
                        elif act == "murder":
                            if randomInt == 5:
                                clientSocket.send(f"{name}: I.. think.. I'm gonna leave..".encode())
                            else:
                                clientSocket.send(f"{name}: I don't think that is a good suggestion right now?".encode())
                        else:
                            if randomInt > 3:
                                clientSocket.send(f"{name}: We don't have time for that!".encode())
                            else:
                                clientSocket.send(f"{name}: We should prioritize getting some work done".encode())

def main():
    # Randomized the mood from the mood array
    ran = random.choice(tuple(moodArray))

    # Creates a bot that has the correct alphabetical name based on the amount of clients, and a random mood
    bot(nameArray[int(teller)], ran)

if __name__ == '__main__':
    # Avaiable to be run through the command windows with the command ../../client.py main
    # Replace ../../ with the correct path of the file in the structure
    main()