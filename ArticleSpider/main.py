from scrapy.cmdline import execute
import sys
import os
#获取当前文件的父目录,__file__指main.py这个文件
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#命令行下的命令
execute(["scrapy","crawl","jobbole"])


