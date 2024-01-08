import os
from datetime import datetime
from urllib.parse import urlparse
import sys
import socket
def download_file_in_blocks(url, block_size=1024*1024):
    parsed_url = urlparse(url)
    file_name = parsed_url.path.split("/")[-1] or str(datetime.now().timestamp()) + ".bin"

    host = parsed_url.netloc
    path = parsed_url.path if parsed_url.path else '/'

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, 80))
        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"
        s.sendall(request.encode())
        response = b''
        while True:
            data = s.recv(block_size)
            if not data:
                break
            response += data
        content_start = response.find(b'\r\n\r\n') + 4
        with open(file_name, 'wb') as file:
            file.write(response[content_start:])
            print(f"File '{file_name}' downloaded successfully.")

    except Exception as e:
        print(f"Failed to download file from {url}: {e}")
    finally:
        if s:
            s.close()

if len(sys.argv) > 2:
    download_file_in_blocks(sys.argv[1], int(sys.argv[2]))
else:
    download_file_in_blocks(sys.argv[1])

#python3 MultiBlockDownloader.py http://fsn.icmp.hetzner.com/1GB.bin 8388608
#python3 MultiBlockDownloader.py http://www.zoomify.com/assets/thumbnails/thmbExpressLg.jpg 8388608
