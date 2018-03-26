from scapy import *

sniff(filter="",iface="any",prn=function,count=N)
def packet_callback(packet):
	print(packet.show())
sniff(prn=packet_callback,count=1)