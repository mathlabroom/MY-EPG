import requests
import gzip
import shutil
import re
from datetime import datetime, timedelta # 补全缺失的引用

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
    # 获取原始文本数据
    data1 = requests.get(url1, timeout=60).text.strip()
    data2 = requests.get(url2, timeout=60).text.strip()
    data3 = requests.get(url3, timeout=60).text.strip()
    
    print("正在直接拼接数据块...")
    with open('guide.xml', 'w', encoding='utf-8') as f:
        # 1. 写入 data1 (保留其完整的 xml 头和 <tv> 标签)
        f.write(data1.rstrip('</tv>').rstrip() + "\n")
        
        # 2. 写入 data2 的内容 (去掉 <tv> 开头和 </tv> 结尾)
        # 匹配 <tv...> 到 </tv> 中间的内容
        import re
        # 将 data2 中 <tv...>(</tv> 之间的部分切出来
        content2 = re.sub(r'(?s).*?<tv[^>]*>(.*?)</tv>.*', r'\1', data2)
        f.write(content2.strip() + "\n")
        
        # 3. 写入 data3 的内容 (同样切出来)
        content3 = re.sub(r'(?s).*?<tv[^>]*>(.*?)</tv>.*', r'\1', data3)
        f.write(content3.strip() + "\n")
            
        # 4. 补齐闭合标签
        f.write('</tv>')
    
    print("guide.xml 生成完毕。正在压缩...")
    with open('guide.xml', 'rb') as f_in, gzip.open('guide.xml.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    print("全部完成！")

if __name__ == "__main__":
    merge_epg()
