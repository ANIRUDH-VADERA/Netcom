# Importing the socket module
import socket
# For distributing the messsages along all clients
import select
# When no message recieved or any other communication error
import errno
import sys
# For realtime updation of state
import threading
import time

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

sequence = []

accepted = []

m = int(clientSocket.recv(128).decode().strip())

for i in range(0,(2**m)):
    sequence.append(i)
Rn = 0
Rf = 0

total_frames = int(clientSocket.recv(1).decode().strip())

for i in range(total_frames):
    accepted.append(0)

# recieving chunks of data from the server
def recieveData():
    flag = 0
    global Rn,Rf,total_frames,accepted
    # Recieving things infinitely
    while (total_frames!=0):
        if(flag == 0):# For the initial informative message
            msg = clientSocket.recv(128).decode()
            print(f"Server > {msg}")        
            flag = 1
        else:# For the subsequent messages
            message = clientSocket.recv(9).decode()
            if(accepted[int(message[-1])]==1):
                print("Frame discarded : Frame ",(message[-1]))
            else:
                if((Rf-Rn)<=(2**(m-1)-1) and (Rf<=(2**m-1))):
                    if(int(message[-1])==Rn):
                        if(Rf>Rn):
                            accepted[Rn] = 1
                            temp = 0
                            for i in range(Rn,Rn+(2**(m-1))+1):
                                if(accepted[i] == 0):
                                   temp = i
                                   break
                            if(message):
                                total_frames = total_frames - temp + Rn + 1
                            print(f"Recieved frame from Server: {message}")
                            print("Number of Jumped frame_acknowledgement : ",temp-Rn)
                            Rn = temp
                            if(int(message[-1])<(2**m-1)):
                                ack_message = "Ack : " + str(sequence[Rn])
                                clientSocket.send(ack_message.encode())
                        else:
                            if(message):
                                total_frames = total_frames - 1
                            accepted[Rf] = 1
                            Rf = Rf + 1
                            Rn = Rn + 1
                            temp_flag_resent = 0
                            if(total_frames!=0):
                                if(int(message[-1])<(2**m-1)):
                                    # if(Rn!=2 and Rn!=3):
                                    #     if(temp_flag_resent==0 and Rn==2):
                                    #         temp_flag_resent = 1
                                    ack_message = "Ack : " + str(sequence[Rn])
                                    clientSocket.send(ack_message.encode())
                                print(f"Recieved frame from Server: {message}")
                    else:
                        if(int(message[-1])>Rn):
                            accepted[int(message[-1])] = 1    
                            if(int(message[-1])>Rf):
                                Rf = int(message[-1])
                            if(message):
                                total_frames = total_frames - 1
                            print(f"Recieved frame from Server: {message}")
                            if(int(message[-1])<(2**m-1)):
                                ack_message = "Nak : " + str(sequence[Rn])
                                clientSocket.send(ack_message.encode())
                            print("Negative Acknowldgement Sent of frame : ",sequence[Rn])

    else:
        print("All the frames were recieved successfully")


recieveThread = threading.Thread(target = recieveData, args=())
recieveThread.start()     