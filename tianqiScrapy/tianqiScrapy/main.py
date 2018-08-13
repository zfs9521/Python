# -*- coding: utf-8 -*-
import os
import sys
from scrapy.cmdline import execute
filename=os.path.dirname(os.path.abspath(__file__))
sys.path.append(filename)
execute(['scrapy','crawl','tianqiSpider'])