import socket
import struct

MCAST_GRP = '225.4.5.6'
MCAST_PORT = 9000

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Allow multiple copies of the same program to receive copies of the multicast datagrams
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the port
sock.bind(('', MCAST_PORT))

# Tell the operating system to add the socket to the multicast group
mreq = struct.pack('4sL', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Receive/respond loop
while True:
    data, address = sock.recvfrom(1024)
    print(data.decode('utf-8'))
