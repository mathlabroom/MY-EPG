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
            # 逻辑：只修正日期，把 stop 的日期强行对齐到 start 的日期
            # 如果节目跨天（比如从 23:00 到 01:00），则 stop 的日期应该是 start+1 天
            # 这里我们检测时间差，如果 stop 的 HHMMSS 小于 start 的 HHMMSS，说明它跨了天
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
    
    print("下载数据...")
    data1 = requests.get(url1, timeout=60).text
    data2 = requests.get(url2, timeout=60).text
    
    # 提取 channel 和 programme
    channel_pattern = re.compile(r'(<channel.*?>.*?</channel>)', re.DOTALL)
    # 捕获 start 和 stop 属性以便修复
    prog_pattern = re.compile(r'(<programme start="(.*?)" stop="(.*?)".*?>.*?</programme>)', re.DOTALL)
    
    print("正在合并并修复时间 Bug...")
    with open('guide.xml', 'w', encoding='utf-8') as f:
        # 写入头部
        xml1_clean = re.sub(r'</tv>\s*$', '', data1.strip())
        f.write(xml1_clean + "\n")
        
        # 写入第二个文件的 Channels
        for c in channel_pattern.findall(data2):
            f.write(c + "\n")
            
        # 写入第二个文件的 Programmes 并进行修复
        for match in prog_pattern.finditer(data2):
            full_prog = match.group(1)
            start_val = match.group(2)
            stop_val = match.group(3)
            
            # 调用上面的修复函数
            fixed_stop = get_fixed_time(start_val, stop_val)
            
            # 如果时间被修正了，替换掉字符串中的 stop 部分
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
