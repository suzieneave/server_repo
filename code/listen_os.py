# Imports
import socket
import struct
import fcntl
import subprocess
import sys


def find_ip():
	'''Finds local ip of this server'''
	output = subprocess.check_output(['bash', '-c', 'hostname -I'])
	print (output)
	weird_ip = str(output)
	rel_chars = '0123456789.'
	ip = ''.join([c for c in weird_ip if c in rel_chars])
	print(ip)
	return ip

MCAST_GRP = find_ip()
MCAST_PORT = 12345

def allow_ip_and_mac_to_be_found(HOST = MCAST_GRP, PORT = MCAST_PORT):

	print('Computer name: ', socket.gethostname())

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST,PORT))
		s.listen()
		conn, addr =s.accept()
		with conn:
			print('Connected by', addr)
			while True:
				data = conn.recv(1024)
				if not data:
					break
				conn.sendall(data)

def listen_for_bash_command(mcast_grp=MCAST_GRP, mcast_port=MCAST_PORT):
	'''Sets up web socket, listens for bash commands from another device
	on the network running 1_find_ips_for_pis.py'''

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(('', mcast_port))
	mreq = struct.pack("4sl", socket.inet_aton(mcast_grp), socket.INADDR_ANY)
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
			#cmd = "raspistill " + str(rdata.decode())
			cmd = str(rdata.decode())
			pid = subprocess.call(cmd, shell=True)

allow_ip_and_mac_to_be_found()
listen_for_bash_command()
