# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

class RentSpider(scrapy.Spider):
    name = 'rent'
    allowed_domains = ["craigslist.org"]
    start_urls = ['https://philadelphia.craigslist.org/search/apa']

    def parse(self, response):
        rooms = response.xpath('//p[@class="result-info"]')
        for room in rooms:
            post_date = title = room.xpath('time/text()').extract_first()
            title = room.xpath('a/text()').extract_first()
            address = room.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("N/A")[2:-1]
            relative_url = room.xpath('a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)
            deets =  sqft = room.xpath('span[@class="result-meta"]/span[@class="housing"]/text()').extract_first("N/A")
            price = room.xpath('span[@class="result-meta"]/span[@class="result-price"]/text()').extract_first()
            yield{'Posted': post_date, 'Title':title, "Price":price, "Deets": deets, 'Address':address, 'URL':absolute_url}
            # yield{'URL':absolute_url, 'Title':title, 'Address':address}
        relative_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        absolute_next_url = response.urljoin(relative_next_url)

        yield Request(absolute_next_url, callback=self.parse)


            

  
