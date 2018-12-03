# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 10:28:26 2018

@author: dbaleeds
A script to demonstrate how to scrape quotes from Brainy topic page.
"""

import scrapy


class QuotesBrainy(scrapy.Spider):
    name = 'QuotesBrainy'

    start_urls = ['https://www.brainyquote.com/topics/']
    
    def parse(self, response):
        # follow links to topic pages
        for href in response.css('a.topicIndexChicklet::attr(href)'):
            yield response.follow(href, self.parse_item)
            
            
    def parse_item(self, response):
        # iterate through all quotes
        for quote in response.css('#quotesList .grid-item'):                                       
           yield {
              'text': quote.css('a.oncl_q::text').extract_first(),
              'author': quote.css('a.oncl_a::text').extract_first(),
              'tags': quote.css('.kw-box a.oncl_list_kc::text').extract(),
              'category' : response.css('title::text').re(r'(\w+).*')  
            }
        
        # go through the pagination links to access infinite scroll           
        next_page = response.css('div.bq_s.hideInfScroll > nav > ul > li:nth-last-child(1) a::attr(href)').extract_first()
        if next_page is not None:
          next_page = response.urljoin(next_page)
          yield scrapy.Request(next_page, callback=self.parse_item)