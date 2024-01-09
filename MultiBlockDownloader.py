import socket
import sys
from datetime import datetime

buffer_size = int(4*1024*1024)

def download_file(url, block_size):
    parts = url.split("/")
    host = parts[2]
    path = "/" + "/".join(parts[3:])
    port = 80
    filename = ""
    time = datetime.now()
    if parts[3] != "":
        filename = parts[-1]
    else:
        filename = time.strftime("%H_%M_%S")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        head_request = f"HEAD {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"
        s.sendall(head_request.encode())
        responsee = s.recv(1024)
        response = responsee.decode()
        supports_range_requests = "Accept-Ranges: bytes" in response
        print(response)

        if supports_range_requests:
            content_length = int(response.split("Content-Length:")[1].split("\r\n")[0])
            print(content_length)  
            print("Content supports range requests.")
            blocks =(content_length-1)//block_size+1
            with open(filename, "wb") as file:
                for i in range(0, content_length, block_size):
                    range_start = i
                    range_end = min(i + block_size - 1, content_length - 1)
                    get_request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nRange: bytes={range_start}-{range_end}\r\n\r\n"
                    s.sendall(get_request.encode())
                    get_response = b''
                    print(content_length)
                    while len(get_response) < min(block_size, content_length-range_start-1):
                        get_response += s.recv(buffer_size)
                    print(f"Block {range_start//block_size+1}/{blocks} downloaded.")
                    content = get_response.split(b"\r\n\r\n", 1)[-1]
                    file.write(content)
        else:
            request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"
            s.sendall(request.encode())
            content_length = None
            data = b""
            while True:
                response = s.recv(1024)
                if not response:
                    break
                data += response
            content = data.split(b"\r\n\r\n", 1)[-1]
            file.write(content)

    print("\nDownload completed.")

url = sys.argv[1]
block_size = 16 * 1024  # Default block size of 16 MB
download_file(url, block_size)

#python3 MultiBlockDownloader.py http://speedtest.belwue.net/1G
#python3 MultiBlockDownloader.py http://www.zoomify.com/assets/thumbnails/thmbExpressLg.jpg
#8388608