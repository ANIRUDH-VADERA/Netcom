# Importing the socket module
import socket

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

# Now we bind our host machine and port with the socket object we created
# The IPv4 address is given above
# The server is now listening for requests from other host machines also connected to the network
serverSocket.bind((IP,port))

#Listening to requests
serverSocket.listen()
print("ANIRUDH VADERA 20BCE2940")
print("Socket(Server) is currently active and listening to requests!!")

# Stores all those sockets which are connected
socketsList = [serverSocket]
# Client conected
clients = {}

m = int(input("Enter the size of the sequence number field in bits : "))
total_frames = int(input("Enter the total frames to be sent : "))
sequence = []
for i in range(0,(2**m)):
    sequence.append(i)
window_size = 2**m - 1
sf = 0
sn = 0
frames_sent = 1
alarm = 0

# A function to recieve messages from the clients connected over the network
def recieveMessage(clientSocket):
    try:
        return {"Data" : clientSocket.recv(7)}
    except: 
        return False
    
def recieve_ack(notifiedSocket):
    global sf,sn,frames_sent
    while True:           
        if(sf<=sn):
            ack_message = recieveMessage(notifiedSocket)
            if(ack_message['Data'].decode()):
                user = clients[notifiedSocket]
                print(f"{user['Data'].decode()} >> {ack_message['Data'].decode()}")
                if(int(ack_message['Data'].decode()[-1])>=(sf+1) or int(ack_message['Data'].decode()[-1])==0):
                    print("Correct Acknowledgement Recieved")
                    difference = (int(ack_message['Data'].decode()[-1])-(sf))
                    if(difference>=0):   
                        sf = sf + difference
                        frames_sent = frames_sent + difference
                        if(sf>=(2**m-1)):
                            sf = sf - (2**m)
                    else:
                        difference = difference + (2**m)
                        sf = sf + difference
                        frames_sent = frames_sent + difference
                        if(sf>=(2**m-1)):
                            sf = sf - (2**m)
                    if(difference > 1):
                        print("Number of Jumped acknowledgement : ",difference-1)
   
# def timer():
#     global alarm,sf,sn
#     while True:
#         time.sleep(1.5)
#         if(sf!=sn):
#             alarm = (alarm + 1) % 2

# thread3 = threading.Thread(target = timer, args = ())
# thread3.start() 
   
# Making a thread for every user connected to the server
def clientThread(notifiedSocket):
    global sf,sn,frames_sent,total_frames,alarm
    temp_flag = 0
    while (frames_sent!=total_frames):          
        if(alarm==1):
            sn = sf
            alarm = 0
        if((sn-sf)<=(2**m-2) and (sn<=(2**m-1))):
            time.sleep(1)
            message = "Frame : " + str(sequence[sn])
            # if(sn==1 and temp_flag==0):
            #     print("Not sending First Frame for the first time :")
            #     temp_flag = 1
            # else:
            notifiedSocket.send(message.encode())
            sn = sn + 1
            if(sn>=(2**m)):
                sn = sn - (2**m)
    else:
        sf = sf + 1
        print("All the frames were sent successfully")

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
    
    clientSocket.send(str(m).encode())
    
    # Sending the count of total frames
    clientSocket.send(str(total_frames).encode())
    
    msg = "Welcome to the server,Thanks for connecting!!"
    
    # Sending information to client socket
    clientSocket.send(msg.encode())
    

    thread = threading.Thread(target = clientThread, args = (clientSocket,))
    thread.start()
    
    thread2= threading.Thread(target = recieve_ack, args = (clientSocket,))
    thread2.start()
    