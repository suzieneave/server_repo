import socket
import struct
import fcntl
import subprocess
import sys

MCAST_GRP = '192.168.1.167'
MCAST_PORT = 3179

sock = socket.socket(socket.AF_INET socket.SOCK_DGRA, socket.IPPROTO_UDP)
socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind('', MCAST_PORT)
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPROTO_IP, socket.IP_ADDR_MEMBERSHIP, mreq)

print("")
print("3D Scanner - Open source listen script")

debug = 1 #Turn on debug

while True:
	data = sock.recv(10240)
	rdata = data[1:]
	rcmd = ord(data[0])
	if debug == 1:
		print ("Recieved cmd: ", rcmd)
		print("Data: ", rdata)
	if (rcmd == 1):
		print("Shooting")
		cmd = "raspistill " + rdata
		pid = subprocess.call(cmd, shell=True)
