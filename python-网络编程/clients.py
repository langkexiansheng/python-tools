import socket

target_host = "127.0.0.1"
target_port = 99

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((target_host,target_port))

while True:
    datas = input("~:")
    client.send(bytes(datas,encoding='utf8'))
    data = client.recv(4096)
    if str(data,encoding='utf-8'):
        print(str(data,encoding='utf-8'))