# UDPPingerServer.py
# We will need the following module to generate randomized lost packets
import random
from socket import *
import json
import time
import threading

# {'seq_num': 0, 'timestamp': 16778718072989.03, 'message': 'ping 10.0.0.246'}
class packetHandler:
    def __init__(self):
        self.packet_dict = {'seq_num': 0, 'timestamp': 0, 'message': 'init'}
        self.last_time = 0
        self.last_seq = -1
        self.heartbeat = None

    def updateHb(self, new_packet):
        self.packet_dict = new_packet
        self.last_time = time.time_ns()/1000000

        # Check sequence numbers for missing packet
        new_seq = new_packet.get('seq_num')
        if self.last_seq+1 != new_seq and self.last_seq < new_seq:
            print("Packet missing")
        self.last_seq = new_packet.get('seq_num')
    
    def heartbeatRunner(self):
        while True:
            time.sleep(5)
            time_since_last_packet = (time.time_ns()/1000000) - (self.last_time)
            if time_since_last_packet > 9000:
                print("Timeout: no longer recieving packets")






def main():
    # Initialize packet handler and heartbeat thread
    pHandler = packetHandler()
    pHandler.heartbeart = threading.Thread(target=pHandler.heartbeatRunner, args=(), daemon=True)
    pHandler.heartbeart.start()

    # Create a UDP socket
    serverSocket = socket(AF_INET, SOCK_DGRAM)

    # Assign IP address and port number to socket
    serverSocket.bind(('', 12000))
    print("Server listening on port 12000")

    while True:
        # Receive the client packet along with the address it is coming from
        current_packet, address = serverSocket.recvfrom(1024)
        current_packet = json.loads(current_packet)

        # Update values for heartbeat calculations
        pHandler.updateHb(current_packet)

        # Capitalize the message from the client
        message = current_packet.get('message').upper().encode()

        # Generate random number in the range of 0 to 10
        rand = random.randint(0, 10)
        # if rand is less than 4, we consider the packet lost and do not respond
        if rand < 4:
            continue
        # otherwise, the server responds
        serverSocket.sendto(message,address)

if __name__ == "__main__":
    main()