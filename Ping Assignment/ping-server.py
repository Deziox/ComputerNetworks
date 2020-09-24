#Danzel Serrano
#ds867
#section: 007
import sys
import socket
import struct
import random

serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverSocket.bind((serverIP, serverPort))

print("The server is ready to receive on port:  " + str(serverPort) + "\n")

while True:

    data, address = serverSocket.recvfrom(100)

    message = struct.unpack('>hh',data)

    if (random.randint(1, 10) < 4):
        print("Message with sequence number ", str(message[1]), " dropped")
    else:
        print("Responding to ping request with sequence number ", str(message[1]))
        # Echo back to client
        data = struct.pack('>hh', 2, message[1])
        serverSocket.sendto(data, address)

