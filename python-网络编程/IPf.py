#/usr/bin/env python3
# coding : utf-8


"""
主要功能：
	把各种样式的IP段转换成一组单个IP

可以解析的格式：
	192.168.1.1-255
	192.168.1.0/24  ## 2**(32-24) 
	192.168.1.1,3,44,222
	192.168.1.1,192.168.1.3,192.168.1.4
	192.168.1.*
	192.168.1-10.*
	10.10.10.250-10.10.11.3

原理：
	https://blog.csdn.net/qq_17753903/article/details/82794833
"""

from collections.abc import Iterator

# 点分10进制IP转10进制
def ip2num(ip):
	ip=[int(x) for x in ip.split('.')]
	return ip[0] <<24 | ip[1]<<16 | ip[2]<<8 |ip[3]

# 10进制转点分十进制
def num2ip(num):
	return '%s.%s.%s.%s' %( (num & 0xff000000) >>24,(num & 0x00ff0000) >>16, (num & 0x0000ff00) >>8, num & 0x000000ff )

# 获取起始IP
def get_ip(ip):
	start,end = [ip2num(x) for x in ip.split('-') ]
	return [ num2ip(num) for num in range(start,end+1) if num & 0xff ]

# 判断ip分类
class IPf():

	def __init__(self, ips):
		self.ips = ips
		self.employee = []

	def __len__(self):
		if self.ips.count('.') == 3 and '-' in self.ips:
			return len(self.three_points())

		if "/" in self.ips:
			return len(self.subnet_mask())
		#
		if "," or "，" in self.ips:
			return len(self.two_points())

		# IP是否三个点，去掉三个点后是否纯数字
		elif self.ips.count('.') == 3 and self.ips.replace('.','').isdigit():
			return len([self.yuanshi()])

	def __iter__(self):

		if self.ips.count('.') == 3 and '-' in self.ips:
			return MyIterator(self.three_points())

		if "/" in self.ips:
			return MyIterator(self.subnet_mask())
		#
		if "," or "，" in self.ips:
			return MyIterator(self.two_points())

		# IP是否三个点，去掉三个点后是否纯数字
		elif self.ips.count('.') == 3 and self.ips.replace('.','').isdigit():
			return MyIterator([self.yuanshi()])
		

	def yuanshi(self):
		return self.ips

	def three_points(self):
		start_list = []
		end_list   = []

		for i in range(4):
			if '-' in self.ips.split('.')[i]:
				start_list.insert(i,self.ips.split('.')[i].split('-')[0])
				end_list.insert(i,self.ips.split('.')[i].split('-')[1])
			else:
				start_list.insert(i,self.ips.split('.')[i])
				end_list.insert(i,self.ips.split('.')[i])
		return get_ip('.'.join(start_list)+"-"+'.'.join(end_list))

	def two_points(self):
		start_list = []
		ips_list = []

		for i in range(4):
			if ',' in self.ips.split('.')[i]:
				start_list.insert(i,self.ips.split('.')[i].split(','))
			elif '，' in self.ips.split('.')[i]:
				start_list.insert(i,self.ips.split('.')[i].split('，'))
			else:
				start_list.insert(i,[self.ips.split('.')[i]])	

		for i in start_list[0]:
			for ii in start_list[1]:
				for iii in start_list[2]:
					for iiii in start_list[3]:
						ips_list.append(i+"."+ii+"."+iii+"."+iiii)
		return ips_list


	def subnet_mask(self):
		# 暂时未验证输入ip的合法性
		# 192.168.1.5/30
		# int(bin(5).replace(bin(5)[-2:],(32-30)*"1").replace("0b",""),2)
		if '/' in self.ips:
			# 主机位
			host_bits = 32 - int(self.ips.split('.')[3].split('/')[1])
			# 点分10进制IP的第4部分
			ip_4 = int(self.ips.split('.')[3].split('/')[0])
			# 掩码位
			a_mask = int(self.ips.split('.')[3].split('/')[1])
			# 主机所在ip段的开始IP
			start_ips_list = self.ips.split('.')
			start_ips_list[3] = str(int(bin(ip_4).replace(bin(ip_4)[-host_bits:],(32-a_mask)*"0").replace("0b",""),2))
			# 主机所在IP段的结束IP
			end_ips_list = self.ips.split('.')
			end_ips_list[3] =   str(int(bin(ip_4).replace(bin(ip_4)[-host_bits:],(32-a_mask)*"1").replace("0b",""),2))

			return get_ip('.'.join(start_ips_list)+"-"+'.'.join(end_ips_list))

class MyIterator(Iterator):
	def __init__(self, employee_list):
		self.iter_list = employee_list
		self.index = 0


	def __next__(self):
		# 真正返回迭代值的逻辑
		try:
			word = self.iter_list[self.index]
		except IndexError:
			raise StopIteration
		self.index += 1
		return word



# ss = fen2ip('192.168.1.1/24')
# dd = fen2ip('10.33-44.55.2-19')
# ff = fen2ip('10.33.55.2,19,33,456')
# gg = fen2ip("192.168.1.1")
# #
# #
# print("下面打印 dd 的")
# for i in dd:
# 	print(i)
# print("下面打印 ss 的")
# for i in ss:
# 	print(i)
# print("下面打印 ff 的")
# for i in ff:
# 	print(i)
#
# print("下面打印 gg 的")
#
# for i in gg:
# 	print(i)