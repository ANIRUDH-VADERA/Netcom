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

# Function to detect error in hamming code
def detectError(arr, nr):
    n = len(arr)
    res = 0

    # Calculate parity bits again
    for i in range(nr):
        val = 0
        for j in range(1, n + 1):
            if(j & (2**i) == (2**i)):
                val = val ^ int(arr[-1 * j])
 
        # Create a binary no by appending
        # parity bits together.
 
        res = res + val*(10**i)
 
    # Convert binary to decimal
    return int(str(res), 2)


# recieving chunks of data from the server
def recieveData():
    flag = 0
    yn = 1
    while True:
        if(flag == 0):
            msg = clientSocket.recv(128).decode()
            print(f"Server > {msg}")        
            flag = 1
        else:# For the subsequent messages
            r = int(clientSocket.recv(1).decode().strip())
            recievedData = clientSocket.recv(128).decode()
            # x = random.randint(0,len(recievedData)-1)
            # if(int(recievedData[x])==0):
            #     recievedData = recievedData[0:x] + "1" + recievedData[(x + 1):len(recievedData)]
            # else:
            #     recievedData = recievedData[0:x] + "0" + recievedData[(x + 1):len(recievedData)]
            print("The coded data recieved from Sender is : ",recievedData)
            print("Checking if the data is valid : ")
            correction = detectError(recievedData, r)
            if(correction==0):
                print("The recieved coeded data is correct : ")
                actual_data_word = ""
                j = 0
                for i in range(1,len(recievedData)+1):
                    if(i==(2**j)):
                        j = j + 1
                    else:
                        actual_data_word = actual_data_word + recievedData[-1*i]
                print("Hence the actual dataword is : ",actual_data_word[::-1])
                
                print("Do you wish to continue recieving data : ")
                print("1 : Yes")
                print("0 : No")
                yn = input()
                if(int(yn)==0):
                    print("Closing the reciever side : ")
                clientSocket.send(yn.encode())
            else:
                print("The recieved coeded data is incorrect : ")
                print("The position of error is : " , len(recievedData) - correction + 1)
                print("If its a single bit error : ")
                actual_data_word = ""
                j = 0
                for i in range(1,len(recievedData)+1):
                    if(i==(2**j)):
                        j = j + 1
                    else:
                        if(i==correction):
                            if(int(recievedData[-1*i]) == 0):
                                actual_data_word = actual_data_word + "1"
                            else:
                                actual_data_word = actual_data_word + "0"
                        else:
                             actual_data_word = actual_data_word + recievedData[-1*i]
                print("Hence the actual dataword is : ",actual_data_word[::-1])

                print("Do you wish to continue recieving data : ")
                print("1 : Yes")
                print("0 : No")
                yn = input()
                if(int(yn)==0):
                    print("Closing the reciever side : ")
                clientSocket.send(yn.encode())

recieveThread = threading.Thread(target = recieveData, args=())
recieveThread.start()     