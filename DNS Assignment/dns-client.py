#Danzel Serrano
#ds867
#section: 007
import sys
import socket
import struct
import random

server_ip = sys.argv[1]
server_port = int(sys.argv[2])
host_name = sys.argv[3]

clientsocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

for i in range(3):
    try:

        message_id = random.randint(1,100)

        question = host_name + " A IN"

        pack_format = '>hhihh' + str(len(question)) + 's'

        message = struct.pack(pack_format, 1, 0, message_id,len(question),0, question.encode('utf-8')) #no answer

        print("Sending Request to ", server_ip, server_port, ":")
        print("Message ID: ", message_id)
        print("Question Length: ", len(question), "bytes")
        print("Answer Length: 0 bytes")
        print("Question: ", question,"\n")

        clientsocket.sendto(message, (server_ip, server_port))
        clientsocket.settimeout(1)

        data, address = clientsocket.recvfrom(100)
        response_length = len(data.decode())
        response = struct.unpack('>hhihh' + str(response_length - 12) + 's', data)

        # print('response: ', response)
        print("Received Response from", address[0], address[1], ":")
        print("Return Code:", response[1], "(No Errors)" if response[1] == 0 else "(Name does not exist)")
        print("Message ID: ", response[2])
        print("Question Length: ", response[3], "bytes")
        print("Answer Length:", response[4] ,"bytes")

        qa = response[5].decode('utf-8')
        q = qa[0:response[3]]
        a = qa[response[3]:]

        print("Question:", q)
        if(response[1] == 0):
            print("Answer:",a)
        print()
        break

    except socket.timeout:
        print("DNS Request timed out",("\nExiting Program" if i == 2 else ""),'\n')

clientsocket.close()
