# Importing the socket module
import socket
# For distributing the messsages along all clients
import select
# For realtime updation of state
import threading
import time

# AF_INET - IPv4 Connection
# SOCK_STREAM - TCP Connection
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# For allowing reconnecting of clients
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Socket successfully created.")

# IPv4 to be used
# The Binding port no is reserved in my laptop
# Defining the HeaderSize of each message to be sent
IP = "127.0.0.1"  
port = 3000 
HEADERSIZE = 10

# Now we bind our host machine and port with the socket object we created
# The IPv4 address is given above
# The server is now listening for requests from other host machines also connected to the network
serverSocket.bind((IP,port))

#Listening to requests
serverSocket.listen()
print("ANIRUDH VADERA(20BCE2940)")
print("Socket(Server) is currently active and listening to requests!!")

# Stores all those sockets which are connected
socketsList = [serverSocket]
# Client conected
clients = {}

current_acknowledgement = 0


# A function to recieve messages from the clients connected over the network
def recieveMessage(clientSocket):
    try:
        # We add some extra header information to our msg in order to know the size of the message we are sending
        # Getting the message header
        messageHeader = clientSocket.recv(HEADERSIZE)
        if not len(messageHeader):
            return False 
        # Decoding the message length
        messageLength = int(messageHeader.decode().strip())
        # Returning the message and its header
        return {"Header" : messageHeader , "Data" : clientSocket.recv(messageLength)}
    except: 
        return False

# cd OneDrive/Desktop/python
# python reciever_socket_server.py
# python sender_socket_client.py

# Making a thread for every user connected to the server
def clientThread(notifiedSocket,current_acknowledgement,total_frames):
    while True:
        try:          
            initial_message = recieveMessage(notifiedSocket)
            message = recieveMessage(notifiedSocket)
            # The part to do if a client leaves the connection
            if message is False:
                print(f"Closed Connection from {clients[notifiedSocket]['Data'].decode()}")
                socketsList.remove(notifiedSocket)
                del clients[notifiedSocket]
                break
            user = clients[notifiedSocket]
            print(f"Recieved frame from {user['Data'].decode()} : {initial_message['Data'].decode()} :: ",f"Packet : {(int(initial_message['Data'].decode()[-1]))%2}")
            print(f"Recieved message from {user['Data'].decode()} : {message['Data'].decode()}")
        

            if(int(initial_message['Data'].decode()[-1]) == current_acknowledgement ):
                print("Correct Frame Recieved")
                current_acknowledgement = current_acknowledgement + 1
                ack_message = ("Ack" + str(current_acknowledgement)).encode()
                ackMessageHeader = f"{len(ack_message):<{HEADERSIZE}}".encode()    
            
                userName = "Server".encode()
                userNameHeader = f"{len(userName):<{HEADERSIZE}}".encode()    
            
               
                if(current_acknowledgement!=total_frames):
                    notifiedSocket.send(ackMessageHeader + ack_message + userNameHeader + userName)
                else:
                    ack_message = ("error1").encode()
                    ackMessageHeader = f"{len(ack_message):<{HEADERSIZE}}".encode()    
                    notifiedSocket.send(ackMessageHeader + ack_message + userNameHeader + userName)
            else:
                if(int(initial_message['Data'].decode()[-1]) == current_acknowledgement - 1 ):
                    print("Discarding the Previous repeated frame")
                    ack_message = ("Ack" + str(current_acknowledgement)).encode()
                    ackMessageHeader = f"{len(ack_message):<{HEADERSIZE}}".encode()    
                
                    userName = "Server".encode()
                    userNameHeader = f"{len(userName):<{HEADERSIZE}}".encode()    
                
                    notifiedSocket.send(ackMessageHeader + ack_message + userNameHeader + userName)
        
        except:
            print(f"Closed Connection from {clients[notifiedSocket]['Data'].decode()}")
            if(current_acknowledgement==total_frames):
                print("All the frames were successfully recieved")
            socketsList.remove(notifiedSocket)
            del clients[notifiedSocket]
            break



# Listening to requests infinitely untill interupted
while True:
        # Accepting the user and storing its address in the below defined variables
        clientSocket, clientAddress = serverSocket.accept()
       
        # Getting the information user wants to send
        user = recieveMessage(clientSocket)
        if user is False:
            continue
        socketsList.append(clientSocket)
        clients[clientSocket] = user
        
        print(f"Connection from {clientAddress} has been established!! : UserName : {user['Data'].decode()}") 
            
        
        total_frames_message = recieveMessage(clientSocket)
        total_frames = int(total_frames_message['Data'].decode())
        
        # We add some extra header information to our msg in order to know the size of the message we are sending
        # The message to be sent
        msg = "Welcome to the server,Thanks for connecting!!"
        # Adding the length of the message as the header information
        msg = f'{len(msg):<{HEADERSIZE}}' + msg
        
        # Sending information to client socket
        clientSocket.send(msg.encode())

        thread = threading.Thread(target = clientThread, args = (clientSocket,current_acknowledgement,total_frames))
        thread.start()