import random
import time
import sys
from socket import *

client_socket = socket(AF_INET, SOCK_DGRAM)
server = ("127.0.0.1", int(12000))
client_socket.settimeout(1)
rtt_array = []
packetNum = 10

for i in range(packetNum):

    start_time = time.time()
    host_name = gethostname()
    server_ip = gethostbyname(host_name)
    msg = 'PING ' + str(server_ip) + " " + str(i)

    try:
        client_socket.sendto(msg.encode(), server)
        client_socket.settimeout(1)

        client_socket.recv(1024)
        end_time = time.time()
        rtt = (end_time - start_time) * 1000
        msg += " " + str(format(rtt, '.3f')) + "ms\n"
        rtt_array.append(rtt)
        print(msg)

    except timeout:
        timeout_msg = "Request timed out"
        print(timeout_msg)
        
print("Max RTT: " + str(max(rtt_array)))
print("Min RTT: " + str(min(rtt_array)))
print("Average RTT: " + str(sum(rtt_array) / len(rtt_array)))

packetLossPercent = (1 - (len(rtt_array) / packetNum)) * 100
print(f"Packet loss is {packetLossPercent}%")

