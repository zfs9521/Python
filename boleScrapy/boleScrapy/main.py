# -*- coding: utf-8 -*-
import os
import sys
from scrapy.cmdline import execute
dirfile=os.path.dirname(os.path.abspath(__file__))
sys.path.append(dirfile)
execute(['scrapy','crawl','bole'])