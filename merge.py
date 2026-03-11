import requests
import re
import os

def process_epg_from_urls():
    # 1. 下载两个 XML 数据
    url1 = 'https://raw.githubusercontent.com/dbghelp/SKY-PerfecTV-EPG/refs/heads/main/perfectv.xml'
    url2 = 'https://animenosekai.github.io/japanterebi-xmltv/guide.xml'
    
    print("下载中...")
    data1 = requests.get(url1, timeout=60).text
    data2 = requests.get(url2, timeout=60).text
    
    # 2. 合并：先拼接 data1 和 data2 (剔除 data2 的 xml 头和 tv 头)
    # 这样我们的处理对象就变成了一个超大的 xml
    data2_body = re.sub(r'<\?xml.*?\?>|<tv.*?>|<\/tv>', '', data2)
    merged_data = data1.replace('</tv>', '') + '\n' + data2_body + '\n</tv>'
    
    # 3. 使用你验证通过的逻辑进行提取和追加
    # 为了避免把 <tv> 标签也读进去，我们只提取 programme 部分
    pattern = re.compile(r'(<programme.*?>.*?</programme>)', re.DOTALL)
    
    with open('guide.xml', 'w', encoding='utf-8') as f_out:
        # 第一步：写入合并后的基础内容 (已去最后的 </tv>)
        f_out.write(merged_data.replace('</tv>', '').strip() + "\n")
        
        # 第二步：遍历并追加所有包含 <desc> 的块
        good_ones = pattern.findall(merged_data)
        count = 0
        for prog in good_ones:
            if '<desc' in prog:
                f_out.write(prog + "\n")
                count += 1
        
        # 最后补上结束标签
        f_out.write("</tv>\n")
        print(f"处理完成！追加了 {count} 个描述块。")

if __name__ == "__main__":
    process_epg_from_urls()
