import socket
import os

#host
host = "192.168.1.104"
#create orginal socket and bind in public port
if os.name == "nt":
	socket.protocol = socket.IPPROTO_IP
else:
	socket_protocol = socket.IPPROTO_ICMP
sniffer = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocol)
sniffer.bind((host,0))

sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
print(sniffer.recvfrom(65565))

