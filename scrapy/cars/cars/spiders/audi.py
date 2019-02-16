# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy
import re

#create a scrapy item 


class AudiSpider(CrawlSpider):
    name = 'audi'
    allowed_domains = ['www.cars-data.com']
    start_urls = ['http://www.cars-data.com/en/audi/']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.models .col-4 a',)),
             callback="parse_brand",
             follow=True),)

    def parse_brand(self, response):
        print('Processing..' + response.url)

        #get model links
        m_links = response.css(".modeli::attr(href)").extract()

        for link in m_links:
            yield scrapy.Request(link, callback=self.parse_model)

    def parse_model(self, response):
        print("Processing...", response.url)

        #get type links
        t_links = response.css("table.carData a::attr(href)").extract()

        for link in t_links:
            yield scrapy.Request(link, callback=self.parse_type)

    def parse_type(self, response):
        print("Processing...", response.url)

        #get data
        datas = response.css("table.carData tr td::text").extract()

        #create a new empty dictionary to save data
        details = {}

        for i in range(0,len(datas),2):

            #pre-process key
            key = self.preprocess_key(datas[i])

            #save data to corresponding key
            details[key] = datas[i+1]
        

    
    def preprocess_key(self, key):
        
        #strip whitespace and convert to lower case
        temp = key.strip().lower()

        #remove special characters and whitespaces
        temp = re.sub("[^a-z0-9]+","_", temp)

        #remove trailing '_' if any
        temp = re.sub("_$","",temp)

        return temp
    



        
        
