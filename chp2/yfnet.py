import sys
import socket
import getopt
import threading
import subprocess

#define some global var
listen             = False
command            = False
upload             = False
execute            = ""
target             =""
uploda_destination = ""
port               = 0

#directons for use
def usage():
	print("YYF Net Tool")
	print()
	print("Usage:yfnet.py -t target_host -p port")
	print("-l --listen              - listen on [host]:[port] for incoming connection")
	print("-e --execute=file_to_run - execute the given file upon receiving a connection")
	print("-c --command             - initialize a command shell")
	print("-u --upload=destination  - upon receiving connection upload a file and write to [deatiantion]")
	print()
	print()
	print("Examples:")
	print("yfnet.py -t 192.168.0.1 -p 5555 -l -c")
	print("yfnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
	print("yfnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
	print("echo 'abcdefg' | ./yfnet.py -t 192.168.11.12 -p 135")
	sys.exit(0)

def client_sender(buffer):
	client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		client.connect((target,port))
		if len(buffer):
			client.send(buffer.encode())
		while  True:
			recv_len = 1
			response = ""
			
			while recv_len:
				data = client.recv(4096)
				recv_len = len(data)
				response = response + data.decode()
				
				if recv_len < 4096:
					break
			#waiting for more input
			print(response)
			buffer = input("")
			buffer += "\n"
			client.send(buffer.encode())
	except Exception as err:
		print(err)
		print("[*] Exception Exiting!")
	finally:
		client.close()
#as server
def server_loop():
	global target
	global port

	#if you don't define your target,then we listen to all interface
	if not len(target):
		target = "0.0.0.0"
	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server.bind((target,port))
	server.listen(5)

	while True:
		#socket.accept() accept a tcp connection from client and return a new socket and the client's address
		client_socket,addr = server.accept() 
		client_thread = threading.Thread(target=client_handler,args=(client_socket,))
		client_thread.start()

def client_handler(client_socket):
	global execute
	global upload
	global command

	if len(uploda_destination):
		file_buffer = ""

		while True:
			data = client_socket.recv(1024)
			if not data:
				break
			else:
				file_buffer += data
		try:
			with open(uploda_destination,"wb") as f:
				f.write(file_buffer)
			client_socket.send("Success to save file to %s!\n" %uploda_destination)
		except:
			print("Failed to save file to %s!\n" % uploda_destination)

	if len(execute):
		output = run_command(execute)
		client_socket.send(output)

	if command:
		while True:
			client_socket.send(b"<yyf@ubuntu:#> ")
			cmd_buffer = ""
			while "\n" not in cmd_buffer:
				cmd_buffer += client_socket.recv(1024).decode()
				response = run_command(cmd_buffer)
				client_socket.send(response)

def run_command(command):
	command = command.rstrip()
	try:
		output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
	except:
		output = b"Failed to execute command.\n"
	return output
def main():
	global listen
	global port
	global execute
	global command
	global uploda_destination
	global target

	if not len(sys.argv[1:]):   #filter the first parameter because it's the script's name
		usage()
	try:
		#hle:t:p:cu ":" said that h,t,p... should bring with a patameter behind of it
		opts,args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:",["help","listen","execute","target","port","command","upload"])
	except getopt.GetoptError as e:
		print(str(e))
		usage()
	for o,a in opts:
		if o in ("-h","--help"):
			usage()
		elif o in ("-l","--listen"):
			listen = True
		elif o in ("-p","--port"):
			port = int(a)
		elif o in ("-e","--execute"):
			execute = True
		elif o in ("-c","--commandshell"):
			command = True
		elif o in ("-u","--upload"):
			uploda_destination = a
		elif o in ("-t","--target"):
			target = a
		else:
			assert False,"Unhandled Option"

	#judge listen to the target or only send datas in standard input
	if not listen and len(target) and port > 0:      #only send datas
		buffer = sys.stdin.read()      #read datas from command line
 		#send datas
		client_sender(buffer)
	if listen:
		server_loop()

main()

