import os
from datetime import datetime
from urllib.parse import urlparse
import sys
import socket

def download_file(url):
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
            data = s.recv(1024)
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

if len(sys.argv) > 1:
    download_file(sys.argv[1])
else:
    print("Please provide a valid URL as an argument.")

download_file(sys.argv[1])

#python3 OneBlockDownloader.py http://fsn.icmp.hetzner.com/1GB.bin
#python3 OneBlockDownloader.py http://www.zoomify.com/assets/thumbnails/thmbExpressLg.jpg
#python3 OneBlockDownloader.py http://speedtest.belwue.net/1G