import requests
import re
import gzip
import shutil

def merge_epg():
    url1 = 'https://raw.githubusercontent.com/dbghelp/SKY-PerfecTV-EPG/refs/heads/main/perfectv.xml'
    url2 = 'https://mathlabroom.github.io/japanterebi-xmltv/guide.xml'
    
    print("下载数据...")
    data1 = requests.get(url1, timeout=60).text
    data2 = requests.get(url2, timeout=60).text
    
    # 提取 channel 块和 programme 块的正则
    channel_pattern = re.compile(r'(<channel.*?>.*?</channel>)', re.DOTALL)
    prog_pattern = re.compile(r'(<programme.*?>.*?</programme>)', re.DOTALL)
    
    # 获取 xml2 的所有组件
    channels2 = channel_pattern.findall(data2)
    progs2 = prog_pattern.findall(data2)

    
    # 1. 组装 guide.xml
    print("正在写入 guide.xml...")
    with open('guide.xml', 'w', encoding='utf-8') as f:
        xml1_clean = re.sub(r'</tv>\s*$', '', data1.strip())
        f.write(xml1_clean + "\n")
        for c in channels2:
            f.write(c + "\n")
        for p in progs2:
            f.write(p + "\n")
        f.write('</tv>')
    print("guide.xml 已生成。")

    # 2. 压缩为 guide.xml.gz
    print("正在压缩为 guide.xml.gz...")
    with open('guide.xml', 'rb') as f_in:
        with gzip.open('guide.xml.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print("压缩完成！")

if __name__ == "__main__":
    merge_epg()
