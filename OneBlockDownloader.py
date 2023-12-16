# import socket
# import sys
# import time
# import random

# # Funktion zum Herunterladen der Datei
# def download_file(url):
#     # URL-Zerlegung
#     url_parts = url.split('/')
#     host = url_parts[2]
#     path = '/' + '/'.join(url_parts[3:])

#     # Bestimmen des Dateinamens
#     file_name = url_parts[-1] if url_parts[-1] else f"file_{time.time()}_{random.randint(0, 1000)}" 

#     # Socket-Verbindung zum Server
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect((host, 80))

#     # HTTP GET-Anfrage zusammenstellen
#     request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

#     # Anfrage senden
#     s.sendall(request.encode())

#     # Antwort empfangen
#     response = b''
#     while True:
#         data = s.recv(1024)
#         if not data:
#             break
#         response += data

#     # Trennung von Header und Body
#     header_end = response.find(b'\r\n\r\n')
#     header = response[:header_end]
#     body = response[header_end + 4:]

#     # Header ausgeben
#     print(header.decode())

#     # Datei schreiben
#     with open(file_name, 'wb') as file:
#         file.write(body)

#     # Socket schließen
#     s.close()
#     print(f"Datei '{file_name}' wurde heruntergeladen.")

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Bitte geben Sie eine URL als Kommandozeilenargument an.")
#     else:
#         url = sys.argv[1]
#         download_file(url)
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

    # TCP-Verbindung herstellen
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((hostname, port))

        # HTTP GET-Anfrage senden
        request = f"GET {path} HTTP/1.1\r\nHost: {hostname}\r\n\r\n"
        s.sendall(request.encode())

        # Daten empfangen und Datei schreiben
        received_data = b''
        while True:
            chunk = s.recv(block_size)
            if not chunk:
                break
            received_data += chunk

        # Schreibe die empfangenen Daten in eine Datei
        with open(file_name, 'wb') as file:
            file.write(received_data)
        
        print(f"File '{file_name}' downloaded in blocks of {block_size} bytes.")

# Beispiel-Nutzung:
download_file_in_blocks('http://speed.hetzner.de/1GB.bin', block_size=8 * 1024 * 1024)  # Blockgröße: 8 MB
