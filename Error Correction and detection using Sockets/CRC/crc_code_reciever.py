# Importing the socket module
import socket

# For realtime updation of state
import threading

import random

# AF_INET - IPv4 Connection
# SOCK_STREAM - TCP Connection
clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# IPv4 to be used
# The port to which the client wants to connect
IP = "127.0.0.1"
port = 3000 


# The client userName
my_userName = input("UserName : ")

# Connect to the server on this machine or locally
# socket.gethostname() to get the hostname of the server
clientSocket.connect((IP,port))
# Sending the username to the server
userName = my_userName.encode()
clientSocket.send(userName)


# Function for binary 2 division
def binary_division(divident,polynomial):
    global remainder
    if(len(divident)==len(polynomial)-1):
        remainder=divident
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


remainder = ""

# recieving chunks of data from the server
def recieveData():
    flag = 0
    yn = 1
    global remainder
    while True:
        # try:
            if(flag == 0):
                msg = clientSocket.recv(128).decode()
                print(f"Server > {msg}")        
                flag = 1
            else:# For the subsequent messages
                len_polynomial = int(clientSocket.recv(1).decode().strip())
                polynomial = clientSocket.recv(len_polynomial).decode()
                recievedData = clientSocket.recv(128).decode()
                # x = random.randint(0,len(recievedData)-len(polynomial)-2)
                # if(int(recievedData[x])==0):
                #     recievedData = recievedData[0:x] + "1" + recievedData[(x + 1):len(recievedData)]
                # else:
                #     recievedData = recievedData[0:x] + "0" + recievedData[(x + 1):len(recievedData)]
                print("The coded data recieved from Sender is : ",recievedData)
                print("Checking if the data is valid : ")
                binary_division(recievedData,polynomial)
                if(int(remainder)==0):
                    print("The recieved coeded data is correct : ")
                    print("Hence the actual dataword is : ",recievedData[:-1*(len(polynomial)-1)])
                    
                    print("Do you wish to continue recieving data : ")
                    print("1 : Yes")
                    print("0 : No")
                    yn = input()
                    if(int(yn)==0):
                        print("Closing the reciever side : ")
                    clientSocket.send(yn.encode())
                else:
                    print("The recieved coeded data is incorrect : ")
                    print("The Syndrome is : " , remainder) 
    
                    print("Do you wish to continue recieving data : ")
                    print("1 : Yes")
                    print("0 : No")
                    yn = input()
                    if(int(yn)==0):
                        print("Closing the reciever side : ")
                    clientSocket.send(yn.encode())

recieveThread = threading.Thread(target = recieveData, args=())
recieveThread.start()     