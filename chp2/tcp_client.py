import socket

target_host = "192.168.1.104"
target_port = 9999
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((target_host,target_port))
client.send(b"my name is yyf")
response = client.recv(4096).decode()
print(response)
