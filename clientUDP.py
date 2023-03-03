import socket
import time
import json

class Packet:
    def __init__(self, seq_num, timestamp, message):
        self.seq_num = seq_num
        self.timestamp = timestamp / 100000
        self.message = message

def main():
    rtt_array = []

    # Set up client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1)

    # Set up server address and port to communicate with
    server = ("127.0.0.1", 12000)

    # Create message to send to server
    address = socket.gethostbyname(socket.gethostname())
    ping_msg = 'ping ' + address

    # Ping the server multiple times
    packets = 15
    for i in range(packets):
        packet = Packet(i,(time.time_ns()/1000000),ping_msg)
        packet = json.dumps(packet, default=vars)

        # Try until there is a timeout error flagged by the socket
        try:

            # Send/recieve message to/from server while tracking time difference for each ping
            client_socket.sendto(packet.encode(), server)
            start_time = time.time_ns()
            msg_from_server = client_socket.recvfrom(1024)
            end_time = time.time_ns()

            # Print message recieved from server with RTT
            rtt = (end_time - start_time)/1000000
            print(f'{msg_from_server[0].decode()} {rtt} ms\n')

            # Add rtt to rtt array for later statistics
            rtt_array.append(rtt)

        except socket.timeout:
            print("Request timed out\n")

    # Calculate and print statistics
    print(f'Max RTT: {max(rtt_array):>10.2f} ms')
    print(f'Min RTT: {min(rtt_array):>10.2f} ms')
    print(f'Average RTT: {sum(rtt_array)/len(rtt_array):>6.2f} ms')

    packetLossPercent = (1 - (len(rtt_array) / packets)) * 100
    print(f'Packet loss:{packetLossPercent:>8.2f}%')


if __name__ == "__main__":
    main()