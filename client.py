import socket
import sys


to_send = sys.argv[1]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.connect(("localhost", 7000))
    server.sendall(bytes(to_send, "utf-8"))
    received = str(server.recv(1024), "utf-8")

print("Received: " + received)