import requests
import re

def merge_epg():
    url1 = 'https://raw.githubusercontent.com/dbghelp/SKY-PerfecTV-EPG/refs/heads/main/perfectv.xml'
    url2 = 'https://animenosekai.github.io/japanterebi-xmltv/guide.xml'
    
    print("正在下载源文件...")
    data1 = requests.get(url1, timeout=60).text
    data2 = requests.get(url2, timeout=60).text
    
    # 提取所有 programme 块
    pattern = re.compile(r'(<programme.*?>.*?</programme>)', re.DOTALL)
    
    # 获取所有的条目
    progs1 = pattern.findall(data1)
    progs2 = pattern.findall(data2)
    
    # 筛选出带描述的条目 (作为补丁)
    desc_patches = [p for p in progs2 if '<desc' in p and not re.search(r'<desc[^>]*>\s*</desc>', p)]
    
    print(f"合并: XML1 ({len(progs1)}) + XML2 ({len(progs2)}) + 补丁 ({len(desc_patches)})")
    
    # 开始写入文件
    with open('guide.xml', 'w', encoding='utf-8') as f:
        # 1. 写入头
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n')
        
        # 2. 写入 XML1 和 XML2 的所有原始条目 (去掉重复的头尾，只写内容)
        # 这里直接遍历写入，确保 XML1+XML2 数据全都在
        for p in progs1:
            f.write(p + "\n")
        for p in progs2:
            f.write(p + "\n")
            
        # 3. 追加补丁 (带描述的条目在最后)
        for p in desc_patches:
            f.write(p + "\n")
            
        # 4. 写入尾
        f.write('</tv>')

if __name__ == "__main__":
    merge_epg()
