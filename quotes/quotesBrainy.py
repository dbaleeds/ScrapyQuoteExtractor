# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 12:07:07 2018

@author: dbaleeds
"""
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


            
class QuotesBrainySpider(scrapy.Spider):
    name = "quotesBrainy"
    allowed_domains = ['brainyquote.com']
    start_urls = ['https://www.brainyquote.com/topics/']
   
    #rules = (
    #  Rule(LinkExtractor(allow=('^\/topics.*', )), callback="parse_item")  
    #)
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_items"
        )
    ]
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse_items(self, response):
      for quote in response.css('#quotesList .grid-item'):                                       
    
        yield {
          'text': quote.css('a.oncl_q::text').extract_first(),
          'author': quote.css('a.oncl_a::text').extract_first(),
          'tags': quote.css('.kw-box a.oncl_list_kc::text').extract(),
          'category' : response.css('title::text').re(r'(\w+).*')  
        }
    

           
     #next_page = response.css('div.bq_s.hideInfScroll > nav > ul > li:nth-last-child(1) a::attr(href)').extract_first()
      # if next_page is not None:
       #   next_page = response.urljoin(next_page)
        #  yield scrapy.Request(next_page, callback=self.parse)
