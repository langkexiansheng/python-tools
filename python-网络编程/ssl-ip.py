#!/usr/bin/env python
#说明：SSL - ip是一种扫描互联网并从证书中提取主机名的工具。此工具可用于扫描云范围以查找系统的主机名。此工具用于研究目的，请确保在扫描前获得适当的批准

def banner():
	print("-" * 70)
	print("""
                        ,--,                                                   
                     ,---.'|                                       ,-.----.    
  .--.--.   .--.--.  |   | :                                   ,---\    /  \   
 /  /    './  /    '.:   : |           .--, .--,            ,`--.' |   :    \  
|  :  /`. |  :  /`. /|   ' :           |\  \|\  \           |   :  |   |  .\ : 
;  |  |--`;  |  |--` ;   ; '           ` \  ` \  `          :   |  .   :  |: | 
|  :  ;_  |  :  ;_   '   | |__          \ \  \ \  \         |   :  |   |   \ : 
 \  \    `.\  \    `.|   | :.'|          , \  , \  \        '   '  |   : .   / 
  `----.   \`----.   '   :    ;          / /` / /` /        |   |  ;   | |`-'  
  __ \  \  |__ \  \  |   |  ./          ` /  ` /  /         '   :  |   | ;     
 /  /`--'  /  /`--'  ;   : ;           | .  | .  /          |   |  :   ' |     
'--'.     '--'.     /|   ,/            ./__/./__/           '   :  :   : :     
  `--'---'  `--'---' '---'                                  ;   |.'|   | :     
                                                            '---'  `---'.|     
                                                                     `---`     
                                                                               
SSL >> IP | A scanning tool for scaping hostnames from SSL certificates.
""")
	print("Usage | python ssl-ip.py [CIDR Range]")
	print("E.X   | python ssl-ip.py 10.100.100.0/24")
	print("-" * 70)

import sys, socket, ssl, requests, ipaddress
from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning, SNIMissingWarning
from socket import socket
from OpenSSL import SSL
from ndg.httpsclient.subj_alt_name import SubjectAltName
from pyasn1.codec.der import decoder as der_decoder
import masscan, errno, os, signal
from functools import wraps
import IPy

# pip install ndg-httpsclient

class TimeoutError(Exception):
	pass

def timeouts(seconds=10, error_message=os.strerror(errno.ETIMEDOUT)):
	def decorator(func):
		def _handle_timeout(signum, frame):
			raise TimeoutError(error_message)

		def wrapper(*args, **kwargs):
			signal.signal(signal.SIGALRM, _handle_timeout)
			signal.alarm(seconds)
			try:
				result = func(*args, **kwargs)
			finally:
				signal.alarm(0)
			return result

		return wraps(func)(wrapper)

	return decorator

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)

@timeouts(10)
def getDomainFromCert(ipAddr, port = 443):
	context = SSL.Context(SSL.TLSv1_METHOD)
	context.set_options(SSL.OP_NO_SSLv2)
	context.set_verify(SSL.VERIFY_NONE, callback)
	sock = socket()
	try:
		ssl_sock = SSL.Connection(context, sock)
		sock.settimeout(0.5)
		ssl_sock.connect((str(ipAddr), port))
	except:
		return False
	try:
		sock.settimeout(None)
		ssl_sock.do_handshake()
		cert = ssl_sock.get_peer_certificate()
		name = cert.get_subject().commonName
		try:
			alt = get_subj_alt_name(cert)
			if not alt:
				alt.append(name)
			return alt
		except:
			return name
	except:
		pass

def get_subj_alt_name(peer_cert):
	dns_name = []
	general_names = SubjectAltName()
	for i in range(peer_cert.get_extension_count()):
		ext = peer_cert.get_extension(i)
		ext_name = ext.get_short_name()
		if ext_name == "subjectAltName":
			ext_dat = ext.get_data()
			decoded_dat = der_decoder.decode(ext_dat, asn1Spec=general_names)

			for name in decoded_dat:
				if isinstance(name, SubjectAltName):
					for entry in range(len(name)):
						component = name.getComponentByPosition(entry)
						dns_name.append(str(component.getComponent()))
	return dns_name

def callback(conn, cert, errno, depth, result):
	if depth == 0 and (errno == 9 or errno == 10):
		return False
	return True

if __name__ == "__main__":  
	banner()
	hosts = sys.argv[1:][0]
	if '-' not in hosts:
		ips = IPy.IP(hosts)

		for ip in ips:
			s = socket()
			s.settimeout(0.1)
			ip = str(ip)
			if s.connect_ex((ip, 443)) == 0:
				s.close()
				print ip ,getDomainFromCert(ip)