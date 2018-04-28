# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,MapCompose,Join

#进行数据的清洗
#获取房子的每平米的价格，面积，建造的年份的数字部分，去掉汉字
def get_num(value):

    if value:
        num = re.match('(\d+)',value).group(1)
        return int(num)
    else:
        num = 0
        return int(num)

#去掉房子结构和楼层中的制表符和换行符
def remove_tags(value):

    str = ''.join(value.split())
    return str


class AnjukeItemLoader(ItemLoader):
    #通过itemloader获取的数据是以列表的形式存在，我们可以通过TakeFirst()的方法把列表中的第一个非空的值转换为字符串
    default_output_processor = TakeFirst()

class AnjukeItem(scrapy.Item):

    price = scrapy.Field(input_processor = MapCompose(get_num))
    mode = scrapy.Field(input_processor = MapCompose(remove_tags))
    area = scrapy.Field(input_processor = MapCompose(get_num))
    floor = scrapy.Field(input_processor = MapCompose(remove_tags))
    year = scrapy.Field(input_processor = MapCompose(get_num))
    location = scrapy.Field()
    district = scrapy.Field()