#Danzel Serrano
#ds867
#section: 007

import sys
import socket
import struct

serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

file = open('dns-master.txt')
dns_master = dict()
for line in file:
    if(line[0] == "#" or len(line.strip()) == 0):
        continue
    rr = line.strip().split(' ')
    dns_master[rr[0]] = rr[1:]

# print(dns_master,"\n\n")
# print('host2.student.test' in dns_master)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((serverIP, serverPort))

print("DNS server is ready to receive on port:  " + str(serverPort) + "\n")

while True:

    data, address = serverSocket.recvfrom(100)

    question_length = len(data.decode())

    message = struct.unpack('>hhihh' + str(question_length - 12) + 's',data)

    question = message[5].decode('utf-8').split(" ")

    if (question[0] in dns_master):
        dn = dns_master[question[0]]
        answer = " ".join(question) + " " + dn[2] + " " + dn[3]

        pack_format = '>hhihh' + str(message[3]) + 's' + str(len(answer)) + 's'
        # print(pack_format, 2 , 0, message[2], message[3],len(answer)," ".join(question),answer, " ".join(question).encode('utf-8'),answer.encode('utf-8'))
        data = struct.pack(pack_format, 2, 0, message[2], message[3],len(answer)," ".join(question).encode('utf-8'),answer.encode('utf-8'))
        serverSocket.sendto(data, address)

    else:
        pack_format = '>hhihh' + str(message[3]) + 's'
        # print(pack_format, 2, 0, message[2], message[3], len(answer), " ".join(question), answer,
        #       " ".join(question).encode('utf-8'), answer.encode('utf-8'))
        data = struct.pack(pack_format, 2, 1, message[2], message[3], 0, " ".join(question).encode('utf-8'))
        serverSocket.sendto(data, address)


