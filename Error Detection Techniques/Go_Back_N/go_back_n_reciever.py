# Importing the socket module
import socket

# For realtime updation of state
import threading


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

m = int(clientSocket.recv(1).decode().strip())

for i in range(0,(2**m)):
    sequence.append(i)
Rn = 0
window_size = 1

total_frames = int(clientSocket.recv(2).decode().strip())

# recieving chunks of data from the server
def recieveData():
    flag = 0
    global Rn,total_frames
    # Recieving things infinitely
    while (total_frames!=0):
        # try:
            if(flag == 0):# For the initial informative message
                msg = clientSocket.recv(128).decode()
                print(f"Server > {msg}")        
                flag = 1
            else:# For the subsequent messages
                message = clientSocket.recv(9).decode()
                if(int(message[-1])==Rn):
                    if(message):
                        total_frames = total_frames - 1
                    Rn = Rn + 1
                    if(Rn>=len(sequence)):
                        Rn = 0
                    if(total_frames!=0):
                        if(Rn!=3):
                            ack_message = "Ack : " + str(sequence[Rn])
                            clientSocket.send(ack_message.encode())
                        else:
                            print("Acknowledgement Lost")
                    print(f"Recieved frame from Server: {message}")
                else:
                    print("No Action",end="   :    ")
                    print("Frame : ",message[-1],"discarded")
    else:
        print("All the frames were recieved successfully")


recieveThread = threading.Thread(target = recieveData, args=())
recieveThread.start()     