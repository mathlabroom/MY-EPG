import requests
import gzip
import shutil
import re
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
    # --- 配置区：在此处管理你的链接 ---
    # 如果只想保留 data3，请注释掉 url1 和 url2
    resource_urls = [
        # 'https://raw.githubusercontent.com/dbghelp/SKY-PerfecTV-EPG/refs/heads/main/perfectv.xml',
        'https://mathlabroom.github.io/japanterebi-xmltv/guide.xml',
        'https://raw.githubusercontent.com/dbghelp/JCOM-TV-EPG/refs/heads/main/jcom.xml',
        'https://github.com/mathlabroom/SKyperfectv-EPG-/releases/download/latest/epg_ultimate.xml'
    ]
    
    print(f"检测到 {len(resource_urls)} 个激活的数据源...")
    
    downloaded_data = []
    for url in resource_urls:
        print(f"正在下载: {url}")
        try:
            content = requests.get(url, timeout=60).text.strip()
            downloaded_data.append(content)
        except Exception as e:
            print(f"下载失败: {e}")

    if not downloaded_data:
        print("没有可用的数据。")
        return

    print("开始处理数据...")
    with open('guide.xml', 'w', encoding='utf-8') as f:
        # 判断：如果数据源大于 1 个，执行 TV 标签处理逻辑
        if len(downloaded_data) > 1:
            print("执行多数据源合并逻辑...")
            # 1. 写入第一个数据，去掉末尾的 </tv>
            first_data = re.sub(r'</tv>\s*$', '', downloaded_data[0])
            f.write(first_data + "\n")
            
            # 2. 写入后续数据，剥离 <tv> 标签
            for i in range(1, len(downloaded_data)):
                inner_content = re.sub(r'(?s).*?<tv[^>]*>(.*?)</tv>.*', r'\1', downloaded_data[i])
                f.write(inner_content.strip() + "\n")
            
            # 3. 补全闭合标签
            f.write('</tv>')
        else:
            print("只有一个数据源，执行直接写入逻辑...")
            # 直接写入，不进行任何 TV 标签剥离
            f.write(downloaded_data[0])
    
    print("guide.xml 生成完毕。正在压缩...")
    with open('guide.xml', 'rb') as f_in, gzip.open('guide.xml.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    print("全部完成！")

if __name__ == "__main__":
    merge_epg()
