# -*- coding: utf-8 -*-
import scrapy
import time
import random
from ..items import AnjukeItem,AnjukeItemLoader

class HouseSpider(scrapy.Spider):
    name = 'house'
    allowed_domains = ['nanjing.anjuke.com/sale/?from=navigation']
    start_urls = ['https://nanjing.anjuke.com/sale/']


    #需要添加默认的头信息，因为网站会进行反爬虫
    custom_settings = {
                        'COOKIES_ENABLED':False,
                        'DOWNLOAD_DELAY': 3.5,
                        'DEFAULT_REQUEST_HEADERS':{
                            ':authority':'nanjing.anjuke.com',
                            ':method':'GET',
                            ':path':'/sale/',
                            ':scheme':'https',
                            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                            'accept-encoding':'gzip, deflate, br',
                            'accept-language':'zh-CN,zh;q=0.9',
                            'cache-control':'no-cache',
                            'cookie':'aQQ_ajkguid=1BF7D638-D23C-9225-C86F-FEC7A1527921; _ga=GA1.2.171959919.1524817244; _gid=GA1.2.175082648.1524817244; 58tj_uuid=a5c06107-d3b2-4349-b73d-ec3c676581c1; als=0; propertys=jkxtq0-p7uc2u_jwg8wo-p7u5lt_jvvnr1-p7u4k8_; lps=http%3A%2F%2Fwww.anjuke.com%2F%3Fpi%3DPZ-baidu-pc-all-biaoti%7Chttps%3A%2F%2Fwww.baidu.com%2Fs%3Fie%3Dutf-8%26f%3D8%26rsv_bp%3D0%26rsv_idx%3D1%26tn%3Dbaidu%26wd%3Danjuke%26rsv_pq%3Da03213250004a487%26rsv_t%3D5311tIcL%252BHdsY1bCoWbnVn6nxvZc5NkYulQsOMZvvsIjBtom0bHmsdzxvaA%26rqlang%3Dcn%26rsv_enter%3D1%26rsv_sug3%3D7%26rsv_sug1%3D4%26rsv_sug7%3D100%26rsv_sug2%3D0%26inputT%3D2225%26rsv_sug4%3D3893; twe=2; sessid=EEA17854-C5F1-5DE6-5998-1FBBDF46B6A9; init_refer=https%253A%252F%252Fwww.baidu.com%252Fs%253Fie%253Dutf-8%2526f%253D8%2526rsv_bp%253D0%2526rsv_idx%253D1%2526tn%253Dbaidu%2526wd%253Danjuke%2526rsv_pq%253Da03213250004a487%2526rsv_t%253D5311tIcL%25252BHdsY1bCoWbnVn6nxvZc5NkYulQsOMZvvsIjBtom0bHmsdzxvaA%2526rqlang%253Dcn%2526rsv_enter%253D1%2526rsv_sug3%253D7%2526rsv_sug1%253D4%2526rsv_sug7%253D100%2526rsv_sug2%253D0%2526inputT%253D2225%2526rsv_sug4%253D3893; new_uv=3; _gat=1; ctid=14; new_session=0',
                            'pragma':'no-cache',
                            'referer':'https://beijing.anjuke.com/sale/?from=navigation',
                            'upgrade-insecure-requests':'1',
                            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
                        }
                    }


    def parse(self, response):

        #获取每一页的房子的url并构成请求对象交给调度器
        for sel in response.css("#houselist-mod-new li"):
            house_urls = sel.xpath('//div[@class="house-title"]/a/@href').extract()
            #随机的产生休眠的时间，防止网站进行反爬虫
            for house_url in set(house_urls):
                sleep_time = random.randint(0,2)+random.random()
                time.sleep(sleep_time)
                yield scrapy.Request(url=house_url,callback=self.parse_house,dont_filter=True)


        #获取下一页url,并构建新的请求对象，就交给parse方法进行解析
        next_page = response.css(".aNxt::attr(href)").extract_first()
        if next_page:
            sleep_time = random.randint(3,5)+random.random()
            time.sleep(sleep_time)
            yield scrapy.Request(url=next_page,callback=self.parse,dont_filter=True)


    def parse_house(self,response):

        #通过itemloader进行解析网页，获得数据
        item_loader = AnjukeItemLoader(item=AnjukeItem(),response=response)
        item_loader.add_xpath('price','//div[@class="third-col detail-col"]/dl[1]/dd/text()')
        item_loader.add_xpath('mode','//div[@class="second-col detail-col"]/dl[1]/dd/text()')
        item_loader.add_xpath('area','//div[@class="second-col detail-col"]/dl[2]/dd/text()')
        item_loader.add_xpath('floor','//div[@class="second-col detail-col"]/dl[4]/dd/text()')
        item_loader.add_xpath('year','//div[@class="first-col detail-col"]/dl[3]/dd/text()')
        item_loader.add_xpath('location','//div[@class="first-col detail-col"]/dl[1]/dd/a/text()')
        item_loader.add_xpath('district','//div[@class="first-col detail-col"]/dl[2]/dd/p/a/text()')

        house_info = item_loader.load_item()
        yield house_info


