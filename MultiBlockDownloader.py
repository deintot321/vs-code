import socket
import os
from datetime import datetime
from urllib.parse import urlparse

def download_file_in_blocks(url, block_size=16 * 1024 * 1024):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    port = parsed_url.port or 80
    path = parsed_url.path or '/'
    file_name = path.split("/")[-1] or str(datetime.now().timestamp()) + ".bin"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((hostname, port))

        request = f"GET {path} HTTP/1.1\r\nHost: {hostname}\r\n\r\n"
        s.sendall(request.encode())

        received_data = b''
        while True:
            chunk = s.recv(block_size)
            if not chunk:
                break
            received_data += chunk

        with open(file_name, 'wb') as file:
            file.write(received_data)
        
        print(f"File '{file_name}' downloaded in blocks of {block_size} bytes.")

#python3 MultiBlockDownloader.py http://fsn.icmp.hetzner.com/1GB.bin 8*1024*1024