

import sys
from googletrans import Translator
translate = Translator()

def fanyi(strs, dest='zh-CN'):

	translate_ = translate.translate(strs,dest=dest)
	return translate_.text


fb = open("漏洞统计_未翻译.csv", 'r')

n = 0
lines = fb.readlines()
fb.close()

tj = open("漏洞统计_已翻译.csv", "a+", encoding='gbk')
// 脚本报错打印一串* 后，复制i的值到1后面，比如： 1+99，然后再次运行程序，
for i, line in enumerate(lines[1:]):
	IP地址, 高危数量, 中危数量, 低危数量, 总计, 漏洞名称, 危险程度, 影响IP, 漏洞描述,修复建议 = line.split(",")
	try:
		name = fanyi(漏洞名称)
		c    = fanyi(危险程度)
		vulu = fanyi(漏洞描述)
		jy   = fanyi(修复建议)

		row = f"{IP地址}, {高危数量}, {中危数量}, {低危数量}, {总计}, {name}, {c}, {影响IP}, {vulu},{jy}"
		row = row.replace("\u200b","")
		print(row)
		tj.write(row+"\n")
	except Exception as e:
		print("********")
		print(i,e)
		print("********")
		sys.exit()

tj.close()