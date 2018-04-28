# -*- coding:utf-8 -*-
#V:Python 3.6.3

import os,sys
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(["scrapy","crawl","house"])