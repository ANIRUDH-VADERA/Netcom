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

# Function for binary 2 division
def binary_division(divident,polynomial):
    global code
    if(len(divident)==len(polynomial)-1):
        code=divident
        return
    temp=divident[0:len(polynomial)]
    if(temp[0]=="0"):
        binary_division(divident[1:],polynomial)
    else:
        temp2=""
        for i in range(len(polynomial)):
            if(temp[i]=="1" and polynomial[i]=="1"):
                temp2+="0"
            if(temp[i]=="1" and polynomial[i]=="0"): 
                temp2+="1"
            if(temp[i]=="0" and polynomial[i]=="1"): 
                temp2+="1"
            if(temp[i]=="0" and polynomial[i]=="0"):
                temp2+="0"
        divident=temp2+divident[len(polynomial):]
        binary_division(divident,polynomial)  

# A function to recieve messages from the clients connected over the network
def recieveMessage(clientSocket):
    try:
        return {"Data" : clientSocket.recv(128)}
    except: 
        return False

flag = 1
check = 0
code=''  

# Making a thread for every user connected to the server
def clientThread(notifiedSocket):
    global flag,check,code
    while True:
        if(check==0):
            
            polynomial=input("Enter the polynomial : ")
            
            data = input("Enter the dataword to be coded : ")
            ss=''
            for i in range(len(polynomial)-1):
                ss+="0"
            divident=data+ss
            binary_division(divident,polynomial)     
            if(len(code)<len(polynomial)-1):
                ss=''
                for i in range(len(polynomial)-1-len(code)):
                    ss+="0"
                code=ss+code    
            data=list(data)
            data="".join(data)  
    
            print("Sending  Polynomial : ")
            notifiedSocket.send(str(len(polynomial)).encode())
            notifiedSocket.send(polynomial.encode())
    
            print("The data after generation of code bits is : ",(data+code))
            print("Sending the coded data to reciever : ")
            notifiedSocket.send((data+code).encode())   
            check = 1
        

def recieve(notifiedSocket):
    global flag,check
    while True:
        # Checking if reciever wants more data
        flag = clientSocket.recv(1).decode().strip()
        flag = int(flag)
        if(int(flag)==0):
            print("Closing the sender side : ")
        if(flag == 0):
            check = 1
        else:
            check = 0
        


# Listening to requests infinitely untill interupted
while (flag!=0):
    # Accepting the user and storing its address in the below defined variables
    clientSocket, clientAddress = serverSocket.accept()
    # Getting the information user wants to send
    user = recieveMessage(clientSocket)
    if user is False:
        continue
    socketsList.append(clientSocket)
    clients[clientSocket] = user  
    print(f"Connection from {clientAddress} has been established!! : UserName : {user['Data'].decode()}") 
    msg = "Welcome to the server,Thanks for connecting!!"  
    # Sending information to client socket
    clientSocket.send(msg.encode())

    thread = threading.Thread(target = clientThread, args = (clientSocket,))
    thread.start()
    
    thread2= threading.Thread(target = recieve, args = (clientSocket,))
    thread2.start()
    

    