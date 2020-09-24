import sys
import socket

host = sys.argv[1]
port = int(sys.argv[2])
count = int(sys.argv[3])
data = 'X' * count

# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

i = 0
while True:
    try:
        # Send data to server
        print("Sending data to   " + host + ", " + str(port) + ": " + data)
        clientsocket.sendto(data.encode(),(host, port))
        clientsocket.settimeout(1)
        i+=1

        # Receive the server response
        dataEcho, address = clientsocket.recvfrom(count)
        print("Receive data from " + address[0] + ", " + str(address[1]) + ": " + dataEcho.decode())
        break

    except socket.timeout:
        print("Message Timed Out")
        if(i == 3):
            break


# Close the client socket
clientsocket.close()
