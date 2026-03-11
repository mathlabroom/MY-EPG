EPG link:https://mathlabroom.github.io/MY-EPG/guide.xml
此EPG整合了两个EPG：
url1 = 'https://raw.githubusercontent.com/dbghelp/SKY-PerfecTV-EPG/refs/heads/main/perfectv.xml'
url2 = 'https://animenosekai.github.io/japanterebi-xmltv/guide.xml'
感谢！
perfectv.xml中没有desc内容。
guide.xml是爬取了两个网站的数据。很可惜的是，两个网站相同频道的channel id是一样的，文件中靠后的programe是没有desc的，所以如果直接导入guide.xml，会后入为主，没有desc,本脚本解决了这一问题：把所有带有desc内容的行，重新写在了文件末尾，bingo！
