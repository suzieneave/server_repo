import socket
import struct
import fcntl
import subprocess
import sys

MCAST_GRP = '192.168.1.198'
MCAST_PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
#sock.setsockopt(socket.IPROTO_IP, socket.IP_ADDR_MEMBERSHIP, mreq)

print("")
print("3D Scanner - Open source listen script")

debug = 1 #Turn on debug

while True:
	data = sock.recv(10240)
	print('data: ', data)
	print('data 0: ', data[0])
	print('type of data: ', type(data))
	rdata = data[2:]
	print('rdata: ', rdata)
	 
	rcmd = ord(str(data[0]))
	print('rcmd: ', rcmd)
	if debug == 1:
		print ("Recieved cmd: ", rcmd)
		print("Data: ", rdata)
	if (data[0] == 1):
		print("Shooting")
		cmd = "raspistill " + str(rdata.decode())
		pid = subprocess.call(cmd, shell=True)
