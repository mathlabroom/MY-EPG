import requests
import re
import gzip
import shutil
from datetime import datetime, timedelta

def get_fixed_time(start_str, stop_str):
    try:
        start_part = start_str.split()[0]
        stop_part = stop_str.split()[0]
        start_dt = datetime.strptime(start_part, "%Y%m%d%H%M%S")
        stop_dt = datetime.strptime(stop_part, "%Y%m%d%H%M%S")
        if stop_dt < start_dt:
            if stop_dt.time() < start_dt.time():
                new_date = start_dt.date() + timedelta(days=1)
            else:
                new_date = start_dt.date()
            fixed_stop_dt = datetime.combine(new_date, stop_dt.time())
            return fixed_stop_dt.strftime("%Y%m%d%H%M%S") + " +0000"
    except:
        pass
    return stop_str

def merge_epg():
    url1 = 'https://raw.githubusercontent.com/dbghelp/SKY-PerfecTV-EPG/refs/heads/main/perfectv.xml'
    url2 = 'https://mathlabroom.github.io/japanterebi-xmltv/guide.xml'
    url3 = 'https://raw.githubusercontent.com/dbghelp/JCOM-TV-EPG/refs/heads/main/jcom.xml'
    
    print("下载数据...")
    data1 = requests.get(url1, timeout=60).text
    data2 = requests.get(url2, timeout=60).text
    data3 = requests.get(url3, timeout=60).text
    
    # 优化后的正则表达式：能匹配所有带属性的标签，无论是否换行
    channel_pattern = re.compile(r'(<channel.*?>.*?</channel>)', re.DOTALL)
    prog_pattern = re.compile(r'(<programme start="(.*?)" stop="(.*?)".*?>.*?</programme>)', re.DOTALL)
    
    print("正在精准合并...")
    with open('guide.xml', 'w', encoding='utf-8') as f:
        # 1. 写入 data1 (去掉结尾标签)
        xml1_clean = re.sub(r'</tv>\s*$', '', data1.strip())
        f.write(xml1_clean + "\n")
        
        # 2. 提取并写入 data2 的内容
        for c in channel_pattern.findall(data2):
            f.write(c + "\n")
        for match in prog_pattern.finditer(data2):
            full_prog, s, e = match.group(1), match.group(2), match.group(3)
            # 执行修复
            fixed_e = get_fixed_time(s, e)
            if fixed_e != e:
                full_prog = full_prog.replace(f'stop="{e}"', f'stop="{fixed_e}"')
            f.write(full_prog + "\n")

        # 3. 提取并写入 data3 的内容 (重点补全这里)
        for c in channel_pattern.findall(data3):
            f.write(c + "\n")
        for match in prog_pattern.finditer(data3):
            full_prog, s, e = match.group(1), match.group(2), match.group(3)
            # 执行修复
            fixed_e = get_fixed_time(s, e)
            if fixed_e != e:
                full_prog = full_prog.replace(f'stop="{e}"', f'stop="{fixed_e}"')
            f.write(full_prog + "\n")
            
        f.write('</tv>')
    
    print("guide.xml 生成完毕。正在压缩...")
    with open('guide.xml', 'rb') as f_in, gzip.open('guide.xml.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    print("全部完成！")

if __name__ == "__main__":
    merge_epg()
