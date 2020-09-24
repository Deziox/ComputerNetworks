#Danzel Serrano
#ds867
#section: 007
import sys
import socket
import time
import struct

server_ip = sys.argv[1]
server_port = int(sys.argv[2])

clientsocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

print("Pinging " + server_ip + ", " + str(server_port) + ": ")

#rtt array
rtt_ary = []

for i in range(1,11):
    try:
        message = struct.pack('>hh', 1, (i))

        send_time = time.time_ns() * (10**-9)
        clientsocket.sendto(message,(server_ip, server_port))
        send_time = (time.time_ns() * (10**-9)) - send_time

        clientsocket.settimeout(1)

        recv_time = time.time_ns() * (10**-9)
        dataEcho, address = clientsocket.recvfrom(100)
        recv_time = (time.time_ns() * (10 ** -9)) - recv_time

        #print(send_time, recv_time)

        rtt = abs(recv_time - send_time)
        rtt_ary.append(rtt)

        print("Ping message number ", str(i), " RTT: ", '{0:.6f}'.format(rtt) ," secs")

    except socket.timeout:
        print("Ping message number " , str(i), " timed out")

clientsocket.close()

#stats
print("\nStatistics:\n","10 packets transmitted, ", str(len(rtt_ary)) , " received, ", str(100 - (len(rtt_ary)/10) * 100), "% packet loss")
print("Min/Max/Av RTT = ", '{0:.6f}'.format(min(rtt_ary)), ' / ', '{0:.6f}'.format(max(rtt_ary)), ' / ', '{0:.6f}'.format(sum(rtt_ary)/len(rtt_ary)), " secs")
