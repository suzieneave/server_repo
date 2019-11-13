import socket 
import subprocess
import re

def find_ip():
	output = subprocess.check_output(['bash', '-c', 'hostname -I'])
	print (output)
	weird_ip = str(output)
	rel_chars = '0123456789.'
	ip = ''.join([c for c in weird_ip if c in rel_chars])
	print(ip)
	return ip

		
HOST = find_ip()
PORT = 12345
print('Computer name: ', socket.gethostname())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST,PORT))
	s.listen()
	conn, addr =s.accept()
	with conn:
		print('Connected by', addr)
		while True:
			data = conn.recv(1024)
#			if not data:
#				break
			conn.sendall(data)
