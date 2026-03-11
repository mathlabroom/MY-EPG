import requests
import re

# 1. 下载两个源文件
url1 = 'https://raw.githubusercontent.com/dbghelp/SKY-PerfecTV-EPG/refs/heads/main/perfectv.xml'
url2 = 'https://animenosekai.github.io/japanterebi-xmltv/guide.xml'

print("正在下载...")
xml1 = requests.get(url1, timeout=30).text
xml2 = requests.get(url2, timeout=30).text

# 2. 从 xml2 中筛选出所有带有完整描述 <desc> 的 <programme> 块
# 只有 desc 标签内有内容（长度 > 5）的才被提取
programmes_with_desc = re.findall(r'<programme.*?>[\s\S]*?<desc[^>]*>.{5,}</desc>[\s\S]*?<\/programme>', xml2)

# 3. 合并逻辑
# 步骤：先取出 xml1 的主体，剔除最后的 </tv>，
# 紧接着拼接上我们筛选出的“增强描述条目”，
# 最后补上 </tv>。
print("正在合并并追加修复条目...")
xml1_clean = xml1.replace('</tv>', '').strip()
final_xml = xml1_clean + '\n' + '\n'.join(programmes_with_desc) + '\n</tv>'

# 4. 保存
with open('guide.xml', 'w', encoding='utf-8') as f:
    f.write(final_xml)

print("处理完毕，文件已生成！")
