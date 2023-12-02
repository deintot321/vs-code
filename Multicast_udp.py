import socket

# Set up the multicast group and port
multicast_group = '225.4.5.6'
port = 9000

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the server address
sock.bind(('', port))

# Tell the operating system to add the socket to the multicast group
group = socket.inet_aton(multicast_group)
mreq = socket.inet_aton('0.0.0.0') + group
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print(f"Waiting for messages in multicast group {multicast_group} on port {port}...\n")

while True:
    # Receive the data and print it
    data, address = sock.recvfrom(1024)  # Buffer size is 1024 bytes
    print(f"Received message from {address}:")
    print(data.decode('utf-8'))  # Assuming messages are in UTF-8 encoding