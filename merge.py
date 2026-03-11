import requests
import re

# 下载源
url1 = 'https://raw.githubusercontent.com/dbghelp/SKY-PerfecTV-EPG/refs/heads/main/perfectv.xml'
url2 = 'https://animenosekai.github.io/japanterebi-xmltv/guide.xml'

print("正在下载...")
xml1 = requests.get(url1, timeout=30).text
xml2 = requests.get(url2, timeout=30).text

# 提取修复内容
print("正在修复...")
# 寻找含有 <desc> 的 programme 块
programmes2 = re.findall(r'<programme.*?>[\s\S]*?<desc[\s\S]*?<\/programme>', xml2)

# 合并
print("正在合并...")
final_xml = xml1.replace('</tv>', '') + '\n' + '\n'.join(programmes2) + '\n</tv>'

# 保存
with open('guide.xml', 'w', encoding='utf-8') as f:
    f.write(final_xml)
print("保存成功！")
