#!/usr/bin/env python3
# -*- code: utf-8 -*-
import socket,threading

bind_ip="0.0.0.0"
bind_port=9999

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((bind_ip,bind_port))  #配置监听端口
server.listen(5)    #开始监听，最大连接数设置为5
print("[*] Listening on %s:%d"%(bind_ip,bind_port))

def handle_client(client_socket):
    request=client_socket.recv(1024).decode()
    print("[*] Received: %s" % request)
    
    client_socket.send(("ACK!").encode())
    
    client_socket.close()
    
while True:
    client,addr=server.accept()
    print("[*] Accepted connection from: %s:%d" % (addr[0],addr[1]))
    
    client_handler=threading.Thread(target=handle_client,args=(client,))   #创建一条线程
    client_handler.start()  #启动线程
    
