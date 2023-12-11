import socket
import sys
import time
import random

# Funktion zum Herunterladen der Datei
def download_file(url):
    # URL-Zerlegung
    url_parts = url.split('/')
    host = url_parts[2]
    path = '/' + '/'.join(url_parts[3:])

    # Bestimmen des Dateinamens
    file_name = url_parts[-1] if url_parts[-1] else f"file_{time.time()}_{random.randint(0, 1000)}"

    # Socket-Verbindung zum Server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 80))

    # HTTP GET-Anfrage zusammenstellen
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

    # Anfrage senden
    s.sendall(request.encode())

    # Antwort empfangen
    response = b''
    while True:
        data = s.recv(1024)
        if not data:
            break
        response += data

    # Trennung von Header und Body
    header_end = response.find(b'\r\n\r\n')
    header = response[:header_end]
    body = response[header_end + 4:]

    # Header ausgeben
    print(header.decode())

    # Datei schreiben
    with open(file_name, 'wb') as file:
        file.write(body)

    # Socket schließen
    s.close()
    print(f"Datei '{file_name}' wurde heruntergeladen.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Bitte geben Sie eine URL als Kommandozeilenargument an.")
    else:
        url = sys.argv[1]
        download_file(url)
