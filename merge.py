import requests
import re

def merge_epg():
    url1 = 'https://raw.githubusercontent.com/dbghelp/SKY-PerfecTV-EPG/refs/heads/main/perfectv.xml'
    url2 = 'https://animenosekai.github.io/japanterebi-xmltv/guide.xml'
    
    print("下载数据...")
    data1 = requests.get(url1, timeout=60).text
    data2 = requests.get(url2, timeout=60).text
    
    # 提取 channel 块和 programme 块的正则
    channel_pattern = re.compile(r'(<channel.*?>.*?</channel>)', re.DOTALL)
    prog_pattern = re.compile(r'(<programme.*?>.*?</programme>)', re.DOTALL)
    
    # 获取 xml2 的所有组件
    channels2 = channel_pattern.findall(data2)
    progs2 = prog_pattern.findall(data2)
    
    # 筛选补丁 (带有效描述的 programme)
    desc_patches = [p for p in progs2 if re.search(r'<desc[^>]*>\s*\S+[\s\S]*?</desc>', p)]
    
    # 组装
    with open('guide.xml', 'w', encoding='utf-8') as f:
        # 1. 写入 xml1 的前部分 (直至第一个 </tv> 之前)
        xml1_clean = re.sub(r'</tv>\s*$', '', data1.strip())
        f.write(xml1_clean + "\n")
        
        # 2. 追加 xml2 的频道定义
        for c in channels2:
            f.write(c + "\n")
            
        # 3. 追加 xml2 的全部节目
        for p in progs2:
            f.write(p + "\n")
            
        # 4. 追加描述补丁
        for p in desc_patches:
            f.write(p + "\n")
            
        f.write('</tv>')
    print("合并完毕：保留了所有频道定义并追加了描述补丁。")

if __name__ == "__main__":
    merge_epg()
