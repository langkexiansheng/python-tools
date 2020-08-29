# coding: utf-8

import re
import os
import sys
import time
from socket import gethostbyname



# if len(sys.argv) < 2:
#     sys.exit("""
#     用法：
#     python3 tk_read.py html报告所在目录""")
# path = sys.argv[1]

# awvs导出的报告所在文件夹
path = r"C:\Users\windows\Desktop\haha"


tj = open("漏洞统计_未翻译.csv", "a+", encoding='gbk')
tj.write('"IP地址", 高危数量, 中危数量, 低危数量, 总计, 漏洞名称, 危险程度, 影响IP, 漏洞描述,修复建议\n')


nn = 1
url_number = 0
for root, dirs, files in os.walk(path):
	# 遍历当前目录所有文件
	for file in files:
		if file[-4:] == 'html':
			# print("读取：", file)
			fb = open(os.path.join(path,file), 'r', encoding="utf-8").read()

			kuais = fb.split('<h2 class="page-break ax-section-title ax-section-title--big">')
			
			for kuai in kuais[1:]:


				host = re.findall(r'column-highlight">Host</td>[\s\S]*?<td>(.*?)</td>', kuai)
				High = re.findall(r'>High</td>[\s\S]*?<td>(\d+)</td>', kuai)
				Medium = re.findall(r'>Medium</td>[\s\S]*?<td>(\d+)</td>', kuai)
				Low = re.findall(r'>Low</td>[\s\S]*?<td>(\d+)</td>', kuai)
				zongji = int(High[0]) + int(Medium[0]) + int(Low[0])
				# print(host[0], High[0], Medium[0], Low[0])
				vulues = re.findall(r'<td><b>Alert group</b></td>[\s\S]*?<b>(.*?)</b></td>[\s\S]*?<td>Severity</td>[\s\S]*?<td>(\w+)</td>[\s\S]*?Description</td>[\s\S]*?<td>([\s\S]*?)</td>[\s\S]*?Recommendations</td>[\s\S]*?<td>([\s\S]*?)</td>', kuai)
				
				for vulue in vulues:

					try:
						if len(vulue) == 4:
							vulue_name = vulue[0]
							vulue_Severity = vulue[1]
							vulue_Description = vulue[2]
							vulue_Repair = vulue[3]
						else:
							if len(vulue[0]) == 4:
								vulue_name = vulue[0][0]
								vulue_Severity = vulue[0][1]
								vulue_Description = vulue[0][2]
								vulue_Repair = vulue[0][3]
							else:
								vulue_name = vulue[0][0][0]
								vulue_Severity = vulue[0][0][1]
								vulue_Description = vulue[0][0][2]
								vulue_Repair = vulue[0][0][3]
					except Exception as e:
						vulue_Severity = "错误"
						vulue_Description = "错误"
						vulue_Repair = "错误"
						print(host[0], vulue_name, e)
					ip = gethostbyname(host[0])
					vulue_Description = vulue_Description.strip().replace("<br/> <br/>","").replace("\n\n","").replace(",","，")
					vulue_Repair = vulue_Repair.strip().replace("<br/>","").replace("\n","").replace(",","，")
					row = f'"{host[0]}", {High[0]}, {Medium[0]}, {Low[0]}, {zongji}, {vulue_name}, {vulue_Severity}, ,{vulue_Description},{vulue_Repair}'
					row = row.replace("\u200b","")
					tj.write(row+"\n")
					print(host[0], vulue_name, nn)
					nn = nn + 1

                url_number += 1
				print("第%d个网站" % url_number)
                
tj.close()