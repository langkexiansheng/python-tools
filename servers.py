# -*- coding: utf-8 -*- 

import socket
import threading

bind_ip   = '127.0.0.1'
bind_port = 99

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((bind_ip,bind_port))
server.listen(5)
print('[*] Listening on %s:%d' % (bind_ip,bind_port))

def handle_client(client_socket):
    while True:
        request = client_socket.recv(1024)
        print("[*] Received: %s" % str(request,encoding='utf-8'))
        client_socket.send(bytes("已成功接收",encoding='utf8'))
        
while True:
    client,addr = server.accept()
    print("[*] Accepted connection from:%s:%d" % (addr[0],addr[1]))
    client_handler = threading.Thread(target=handle_client,args=(client,))
    client_handler.start()