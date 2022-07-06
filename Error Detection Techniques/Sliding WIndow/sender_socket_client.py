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

# Defining the HeaderSize of each message to be recieved 
HEADERSIZE = 10

# The client userName
my_userName = input("UserName : ")

# Connect to the server on this machine or locally
# socket.gethostname() to get the hostname of the server
clientSocket.connect((IP,port))
# No blocking the incoming messages
clientSocket.setblocking(False)

# Sending the username to the server
userName = my_userName.encode()
userNameHeader = f"{len(userName):<{HEADERSIZE}}".encode()
clientSocket.send(userNameHeader + userName)

window_size_total_frames = input("Enter the total number of frames to be sent : ")
# Sending the total frames to the server
window_size_total_frames = window_size_total_frames .encode()
totalFramesHeader = f"{len(window_size_total_frames):<{HEADERSIZE}}".encode()
clientSocket.send(totalFramesHeader + window_size_total_frames)

ack_flag = 1
total_frames = int(window_size_total_frames)
current_frame = 0

# recieving chunks of data from the server
def recieveData(ack_flag,current_frame,total_frames):
    flag = 0
    # Recieving things infinitely
    while (total_frames!=0):
        try:
            if(flag == 0):# For the initial informative message
                initHeader = clientSocket.recv(HEADERSIZE)
                initLength = int(initHeader.decode().strip())
                msg = clientSocket.recv(initLength).decode()
                print(f"Server > {msg}")
                flag = 1
            else:# For the subsequent messages
                
                message = input("")
                if message:
                    if(ack_flag!=0):
                        if(current_frame!=3):           
                            message = message.encode()
                            messageHeader = f"{len(message):<{HEADERSIZE}}".encode()    
                            initial_message = ("Frame" + str(current_frame)).encode()
                            initialMessageHeader = f"{len(initial_message):<{HEADERSIZE}}".encode()
                            ack_flag=0
                            clientSocket.send(initialMessageHeader + initial_message + messageHeader + message)
                            temp = message
                        else:
                            time.sleep(5)
                            print("Waiting for the acknowledgement...")
                            print("Waited 5 seconds ... ")
                            print("The data is lost in between : Resending Data")
                            message = message.encode()
                            messageHeader = f"{len(message):<{HEADERSIZE}}".encode()    
                            initial_message = ("Frame" + str(current_frame)).encode()
                            initialMessageHeader = f"{len(initial_message):<{HEADERSIZE}}".encode()
                            ack_flag=0
                            clientSocket.send(initialMessageHeader + initial_message + messageHeader + message)
                            temp = message
                    else:
                        print("Waiting for the acknowledgement...")
            
            
                ack_header = clientSocket.recv(HEADERSIZE)
                ack_message_length = int(ack_header.decode().strip())
                ack_message = clientSocket.recv(ack_message_length).decode()
                
                
                if(ack_message=="error1"):
                    time.sleep(5)
                    userNameHeader = clientSocket.recv(HEADERSIZE)
                    userNameLength = int(userNameHeader.decode().strip())
                    userName = clientSocket.recv(userNameLength).decode()
                    print("Waited 5 seconds ... Timeout Error")
                    print("No Acknowledgement Recieved : Resending the data")
                    clientSocket.send(initialMessageHeader + initial_message + messageHeader + temp)
                    ack_header = clientSocket.recv(HEADERSIZE)
                    ack_message_length = int(ack_header.decode().strip())
                    ack_message = clientSocket.recv(ack_message_length).decode()
                    ack_recieved = int(ack_message[-1])
                    if(ack_recieved==(current_frame+1)):
                        if(ack_flag==0):
                            print("Correct Acknowledgement Recieved")
                            ack_flag = 1
                        current_frame = current_frame + 1
                        total_frames = total_frames - 1
                    else:
                        print("Wrong Acknowledgement...")
                        
                    userNameHeader = clientSocket.recv(HEADERSIZE)
                    if not len(userNameHeader):
                        print("Connection closed by the Server")
                        sys.exit()
                    
                    userNameLength = int(userNameHeader.decode().strip())
                    userName = clientSocket.recv(userNameLength).decode()
                    
                    ack_number = int(ack_message[-1])%2
                    
                    print(f"{userName} >> {ack_message} :: Acknowledgement for Packet {ack_number}")
                else:   
                    ack_recieved = int(ack_message[-1])
    
                    if(ack_recieved==(current_frame+1)):
                        if(ack_flag==0):
                            print("Correct Acknowledgement Recieved")
                            ack_flag = 1
                        current_frame = current_frame + 1
                        total_frames = total_frames - 1
                    else:
                        print("Wrong Acknowledgement...")
                        
                    userNameHeader = clientSocket.recv(HEADERSIZE)
                    if not len(userNameHeader):
                        print("Connection closed by the Server")
                        sys.exit()
                    
                    userNameLength = int(userNameHeader.decode().strip())
                    userName = clientSocket.recv(userNameLength).decode()
                    
                    ack_number = int(ack_message[-1])%2
                    
                    print(f"{userName} >> {ack_message} :: Acknowledgement for Packet {ack_number}")
                
                        
        except IOError as e:
            # This is normal on non blocking connections - when there are no incoming data, error is going to be raised
            # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
            # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
            # If we got different error code - something happened
            if(e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK):
                print("Reading Error",str(e))
                sys.exit()
            continue
        # except Exception as e:
        #     print("General error",str(e))
        #     sys.exit()
    else:
        print("All the frames were sent successfully")


recieveThread = threading.Thread(target = recieveData, args=(ack_flag,current_frame,total_frames,))
recieveThread.start()        