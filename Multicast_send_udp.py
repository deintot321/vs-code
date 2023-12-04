import socket
import struct
# Set up the multicast group and port
multicast_group = '225.4.5.6'
port = 9000

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set the time-to-live for messages to reach the network segment (optional)
ttl = struct.pack('b', 1)  # TTL of 1 (for local network)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

while True:
    # Get user input
    message = input("Enter message to send: ")

    # Send the message to the multicast group
    sock.sendto(message.encode('utf-8'), (multicast_group, port))
