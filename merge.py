import requests
import re
import gzip
import shutil
from datetime import datetime, timedelta

def get_fixed_time(start_str, stop_str):
    """
    智能修复：如果 stop 日期早于 start，只修正日期部分，保留时分秒
    """
    try:
        start_part = start_str.split()[0]
        stop_part = stop_str.split()[0]
        
        start_dt = datetime.strptime(start_part, "%Y%m%d%H%M%S")
        stop_dt = datetime.strptime(stop_part, "%Y%m%d%H%M%S")
        
        # 如果 stop 在 start 之前，说明日期错乱
        if stop_dt < start_dt:
            if stop_dt.time() < start_dt.time():
                new_date = start_dt.date() + timedelta(days=1)
            else:
                new_date = start_dt.date()
                
            fixed_stop_dt = datetime.combine(new_date, stop_dt.time())
            return fixed_stop_dt.strftime("%Y%m%d%H%M%S") + " +0000"
            
    except Exception as e:
        print(f"修正失败: {e}")
        
    return stop_str

def merge_epg():
    url1 = 'https://raw.githubusercontent.com/dbghelp/SKY-PerfecTV-EPG/refs/heads/main/perfectv.xml'
    url2 = 'https://mathlabroom.github.io/japanterebi-xmltv/guide.xml'
    url3 = 'https://raw.githubusercontent.com/dbghelp/JCOM-TV-EPG/refs/heads/main/jcom.xml'
    
    print("下载数据...")
    data1 = requests.get(url1, timeout=60).text
    data2 = requests.get(url2, timeout=60).text
    data3 = requests.get(url3, timeout=60).text
    
    # 提取 channel 和 programme
    channel_pattern = re.compile(r'(<channel.*?>.*?</channel>)', re.DOTALL)
    prog_pattern = re.compile(r'(<programme start="(.*?)" stop="(.*?)".*?>.*?</programme>)', re.DOTALL)
    
    print("正在合并并修复时间 Bug...")
    with open('guide.xml', 'w', encoding='utf-8') as f:
        # 1. 写入头部和第一个文件内容（去尾）
        xml1_clean = re.sub(r'</tv>\s*$', '', data1.strip())
        f.write(xml1_clean + "\n")
        
        # 2. 写入第二个文件的 Channels 和修复后的 Programmes
        for c in channel_pattern.findall(data2):
            f.write(c + "\n")
        for match in prog_pattern.finditer(data2):
            full_prog, start_val, stop_val = match.group(1), match.group(2), match.group(3)
            fixed_stop = get_fixed_time(start_val, stop_val)
            if fixed_stop != stop_val:
                full_prog = full_prog.replace(f'stop="{stop_val}"', f'stop="{fixed_stop}"')
            f.write(full_prog + "\n")

        # 3. 写入第三个文件的 Channels 和修复后的 Programmes
        for c in channel_pattern.findall(data3):
            f.write(c + "\n")
        for match in prog_pattern.finditer(data3):
            full_prog, start_val, stop_val = match.group(1), match.group(2), match.group(3)
            fixed_stop = get_fixed_time(start_val, stop_val)
            if fixed_stop != stop_val:
                full_prog = full_prog.replace(f'stop="{stop_val}"', f'stop="{fixed_stop}"')
            f.write(full_prog + "\n")
            
        f.write('</tv>')
    
    print("guide.xml 生成完毕。正在压缩...")
    with open('guide.xml', 'rb') as f_in, gzip.open('guide.xml.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    print("全部完成！")

if __name__ == "__main__":
    merge_epg()
