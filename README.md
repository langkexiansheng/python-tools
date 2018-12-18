# python-tools
python小工具
### 0x01 server and client
这两个是socket的最基本用法。
最简单的客户端和服务端。

### 0x02 proxy-tcp
用法：
```
C:\Users\cmd>python proxy-tcp.py -lh 127.0.0.1 -lp 21 -rh 192.168.203.132 -rp 21 -rf
[*] Listening on 127.0.0.1:21
[==>] Received incoming connection from 127.0.0.1:51695
0000 32 32 30 20 28 76 73 46 54 50 64 20 32 2E 33 2E  220 (vsFTPd 2.3.
0010 34 29 0D 0A                                      4)..
[<==] Sending 20 bytes to localhost.
[==>] Received 16 bytes from localhost.
0000 55 53 45 52 20 61 6E 6F 6E 79 6D 6F 75 73 0D 0A  USER anonymous..
[==>] Sent to remote.
······
[==>] Received 6 bytes from localhost.
0000 4C 49 53 54 0D 0A                                LIST..
[==>] Sent to remote.
[*] No more data. Closing connections.
```
### 0x03 netcat
用法：[https://langkexiansheng.github.io/#/posts/py%E7%89%88netcat](https://langkexiansheng.github.io/#/posts/py%E7%89%88netcat)

### 0x04 pm_sshcmd
这个脚本可以用来连接ssh,也可以用来爆破ssh.
运行效果
```
C:\Users\cmd>python3 pm_sshcmd.py
尝试密码： yueshaowen
Authentication failed.
尝试密码： xxoo
Authentication failed.
······
尝试密码： motax
Authentication failed.
尝试密码： toor
破解成功，执行命令 whoami： root
```
