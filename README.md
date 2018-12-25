# python-tools
python小工具
## python-网络编程

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

### 0x05 udp_sniffers
用来监听主机网卡的网络流量，
用法：
```
PS C:\Users\cmd\Desktop> python3 .\udp_sniffers.py
Protocol: UDP 192.168.1.30 -> 192.168.1.127
Protocol: UDP 192.168.1.57 -> 192.168.1.127
Protocol: UDP 192.168.1.80 -> 192.168.1.127
Protocol: UDP 192.168.1.44 -> 192.168.1.127
Protocol: UDP 192.168.1.16 -> 192.168.1.127
Protocol: UDP 192.168.1.30 -> 192.168.1.127
Protocol: UDP 192.168.1.57 -> 192.168.1.127
Protocol: UDP 192.168.1.44 -> 192.168.1.127
Protocol: UDP 192.168.1.16 -> 192.168.1.127
Protocol: UDP 192.168.1.57 -> 192.168.1.127
 退出！
```

### 0x06 mail_sniffer.py
用到的库：scapy
测试邮箱：139邮箱
不同的邮箱调整不同的关键词。
只能抓取没有ssl加密的，大部分默认不用。
演示：
```
C:\Users\cmd\Desktop>python3 mail_sniffer.py
[*] Server: 120.196.212.39
[*] b'C3 LOGIN xxxxxxxxxxx@139.com "xxxxxx"\r\n'
[*] Server: 192.168.1.103
[*] b'C3 OK LOGIN completed\r\n'
[*] Server: 120.196.212.39
[*] b'C3 LOGIN xxxxxxxxxxx@139.com "xxxxxx"\r\n'
[*] Server: 192.168.1.103
[*] b'C3 OK LOGIN completed\r\n'
[*] Server: 120.196.212.39
[*] b'C3 LOGIN xxxxxxxxxxx@139.com "xxxxxx"\r\n'
[*] Server: 192.168.1.103
[*] b'C3 OK LOGIN completed\r\n'
```
### 0x07 arp_attack
没有写命令行，直接在代码里添加需要的参数。
效果：
```
C:\Users\cmd>python3 arp_attack.py
无法获取IP为：192.168.xx.xxx 主机的MAC地址，请检查目标IP是否存活
本机MAC地址是： b2:xx:xx:xx:xx:cc
目标计算机IP地址是： 192.168.xx.xxx
目标计算机MAC地址是： None
网关IP地址是： 192.168.xx.xx
网关MAC地址是： 00:00:xx:00:xx:xx
按任意键继续：
[*] Starting sniffer for 1000 packets

Sent 5 packets.
发送一个客户端包

Sent 5 packets.
发送一个网关包

```
