import requests
import os
from datetime import datetime
from urllib.parse import urlparse

def download_file(url):
    parsed_url = urlparse(url)
    file_name = parsed_url.path.split("/")[-1] or str(datetime.now().timestamp()) + ".bin"
    
    headers = {"Host": parsed_url.netloc}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
            print(f"File '{file_name}' downloaded successfully.")
    else:
        print(f"Failed to download file from {url}")


#python3 OneBlockDownloader.py http://fsn.icmp.hetzner.com/1GB.bin

