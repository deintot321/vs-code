import socket
from datetime import datetime, timezone, timedelta

# input server adress
print("Enter time server name or IP address")
# read input
input_server = input()

# create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# connect to server
server_address = (input_server, 37)

# Send the datagram
udp_socket.sendto(b"", server_address)

# Receive data
data = udp_socket.recvfrom(4)

# Convert data to integer
time_value = int.from_bytes(data, byteorder='big')

# Adjusting
epoch_offset = 2208988800  # seconds between 1970 and 1900
timestamp = time_value - epoch_offset

# Convert to UTC time zone
utc_time = datetime.utcfromtimestamp(timestamp)

# Convert to Berlin time zone
berlin_time = utc_time + timedelta(hours=1)

# Format the time
formatted_time = berlin_time.strftime("%Y-%m-%d\n%H-%M-%S")

print(formatted_time)
