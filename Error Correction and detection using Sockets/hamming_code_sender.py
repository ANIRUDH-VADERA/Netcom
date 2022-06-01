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

# Functions to implement Hamming Code:
def calcRedundantBits(m):
    r = 0
    while((2**r)<(m + r + 1)):
        r = r + 1
    return r;
    

def posRedundantBits(data, r):
 
    # Redundancy bits are placed at the positions
    # which correspond to the power of 2.
    j = 0
    k = 1
    m = len(data)
    res = ''
 
    # If position is power of 2 then insert '0'
    # Else append the data
    for i in range(1, m + r+1):
        if(i == 2**j):
            res = res + '0'
            j += 1
        else:
            res = res + data[-1 * k]
            k += 1
 
    # The result is reversed since positions are
    # counted backwards. (m + r+1 ... 1)
    return res[::-1]

def calcParityBits(arr, r):
    n = len(arr)
 
    # For finding rth parity bit, iterate over
    # 0 to r - 1
    for i in range(r):
        val = 0
        for j in range(1, n + 1):
 
            # If position has 1 in ith significant
            # position then Bitwise OR the array value
            # to find parity bit value.
            if(j!=(2**i)):
                if(j & (2**i) == (2**i)):
                    val = val ^ int(arr[-1 * j])
                    # -1 * j is given since array is reversed
 
        # String Concatenation
        # (0 to n - 2^r) + parity bit + (n - 2^r + 1 to n)
        arr = arr[:n-(2**i)] + str(val) + arr[n-(2**i)+1:]
    return arr
            

# A function to recieve messages from the clients connected over the network
def recieveMessage(clientSocket):
    try:
        return {"Data" : clientSocket.recv(128)}
    except: 
        return False

flag = 1
check = 0

# Making a thread for every user connected to the server
def clientThread(notifiedSocket):
    global flag,check
    while True:
        if(check==0):
            data = input("Enter the dataword to be coded : ")
    
            # Calculate the no of Redundant Bits Required
            m = len(data)
            r = calcRedundantBits(m)
    
            print("The redundancy bits required are : ",r)
    
            # Determine the positions of Redundant Bits
            arr = posRedundantBits(data, r)
    
            # Determine the parity bits
            arr = calcParityBits(arr, r)
    
            print("Sending number of check bits : ")
            notifiedSocket.send(str(r).encode())
    
            print("The data after generation of r bits is : ",arr)
            print("Sending the coded data to reciever : ")
            notifiedSocket.send(arr.encode())
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
    

    