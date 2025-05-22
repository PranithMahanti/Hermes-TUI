import threading
import socket
import subprocess
import re

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.nicks = []

    def __str__(self):
        return f"{self.host}:{self.port}"
    
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.server.bind((self.host, self.port))
        self.server.listen()
    
    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message=message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nick = self.nicks[index]
                self.broadcast(f"{nick} has left the chat!".encode('ascii'))
                self.nicks.remove(nick)
                break

    def recieve(self):
        while True:
            client, address = self.server.accept()
            print(f"Connected with {str(address)}")

            client.send("REQ_NICK".encode('ascii'))
            nick = client.recv(1024).decode('ascii')

            self.nicks.append(nick)
            self.clients.append(client)

            print(f"{nick} has joined the chat!")
            client.send('Connected to the server!\n'.encode('utf-8'))
            self.broadcast(f"{nick} has joined the chat!\n".encode('utf-8'))

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

def get_ip():
    result = subprocess.check_output("ipconfig /all", shell=True, text=True)
    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

    return pattern.search(result)[0]


if __name__ == "__main__":
    hostname = socket.gethostname()
    host = get_ip()
    port = 47777

    print(f"Name: {hostname}\nIP Address: {host}")
 
    server = Server(host=host, port=port)
    server.start()
    server.recieve()

