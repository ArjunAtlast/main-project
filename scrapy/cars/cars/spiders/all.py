# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy
import re

class CarsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    transmission = scrapy.Field()
    no_of_seats = scrapy.Field()
    fuel = scrapy.Field()
    no_of_cylinders = scrapy.Field()
    cylinder_capacity = scrapy.Field()
    max_power = scrapy.Field()
    max_torque = scrapy.Field()
    fuel_tank = scrapy.Field()
    top_speed = scrapy.Field()
    abs_ = scrapy.Field()
    airbag_driver = scrapy.Field()
    airbag_side = scrapy.Field()
    airbag_passenger = scrapy.Field()
    alloy_wheels = scrapy.Field()
    wheelbase = scrapy.Field()
    central_locking = scrapy.Field()
    parking_sensors = scrapy.Field()
    reverse_camera = scrapy.Field()
    maintenance = scrapy.Field()
    general_warranty = scrapy.Field()
    chassis_warranty = scrapy.Field()

class AllSpider(CrawlSpider):
    name = 'all'
    allowed_domains = ['www.cars-data.com']
    start_urls = ['http://www.cars-data.com/en/']
    # start_urls = ['http://www.cars-data.com/en/chevrolet/alero']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('a.a_footer',)),
             callback="parse_item",
             follow=True),)

    def parse_item(self, response):

        print("Processing...", response.url)
        
        item_links = response.css('.models > .col-4 a::attr(href)').extract()

        internal_links = response.css('.types > .col-8 > .row > .col-6 a::attr(href)').extract()

        # print("Models", len(item_links))
        # print("Types", len(internal_links))

        for link in item_links[:2]:
            yield scrapy.Request(link, callback=self.parse_item)
        
        for link in internal_links:
            yield scrapy.Request(link, callback=self.parse_individual)

    def parse_individual(self, response):

        print("Processing...", response.url)

        title = response.css('section.title > .col-10 > h1::text').extract()[0]

        print(title)

        item_heads = response.css('dl.row.box > dt.col-6::text').extract()

        item_values = response.css('dl.row.box > dd.col-6::text').extract()

        # print("Heads", len(item_heads))
        # print("Values", len(item_values))

        details = {}

        for i in range(0, len(item_heads)):

            # Preprocess key

            name = item_heads[i]
            temp = name.strip().lower()
            temp = re.sub("[^a-z0-9]+", "_", temp)
            temp = re.sub("_$", "", temp)

            # Preprocess key ends

            details[temp] = item_values[i].strip()

        # Store Data
        
        item = CarsItem()

        item['name'] = re.sub('specs', '', title).strip()
        item['price'] = re.sub("[^0-9\.]","",details['price'])                   #Euro
        item['transmission'] = details['transmission']
        item['no_of_seats'] = re.sub("[^0-9]","",details['number_of_seats'])    #Nos
        item['fuel'] = details['fuel']                     
        item['no_of_cylinders'] = re.sub("[^0-9]","",details['number_of_cylinders'])    #Nos
        item['cylinder_capacity'] = re.sub("[^0-9\.]","",details['cylinder_capacity'])    #cc
        item['max_power'] = details['max_power']                                #kW / hp
        item['max_torque'] = re.sub("[^0-9\.]","",details['max_torque'])          #Nm
        item['fuel_tank'] = re.sub("[^0-9\.]","",details['fuel_tank'])            #Litre
        item['top_speed'] = re.sub("[^0-9\.]","",details['top_speed'])            #km/hr
        item['abs_'] = self.boolean_extract(details['abs'])
        item['airbag_driver'] = self.boolean_extract(details['airbag_driver'])
        item['airbag_side'] = self.boolean_extract(details['side_airbags'])
        item['airbag_passenger'] = self.boolean_extract(details['passenger_airbag'])
        item['alloy_wheels'] = self.boolean_extract(details['alloy_wheels'])
        item['wheelbase'] = details['wheelbase']
        item['central_locking'] = self.boolean_extract(details['central_locking'])
        item['parking_sensors'] = self.boolean_extract(details['parking_sensors'])
        item['reverse_camera'] = self.boolean_extract(details['reverse_camera'])
        item['maintenance'] = self.maintenance_extract(details['maintenance'])  #
        item['general_warranty'] = self.maintenance_extract(details['general_warranty'])
        item['chassis_warranty'] = self.maintenance_extract(details['chassis_warranty'])

        yield item

    def boolean_extract(self, data):
        """
        Gives 1 or 0 output for data
        """
        if not data:
            return 0
        elif data.lower().find('no') != -1:
            return 0
        else:
            return 1
    
    def maintenance_extract(self, data):
        """
        Convert year in put as blank
        """
        if not data:
            return 'NA'
        elif data.lower().find('year'):
            return ''
        else:
            return re.sub("[^0-9]\.", "", data)


## Details to consider
"""
price = scrapy.Field()
transmission = scrapy.Field()
no_of_seats = scrapy.Field()
fuel = scrapy.Field()
no_of_cylinders = scrapy.Field()
cylinder_capacity = scrapy.Field()
max_power = scrapy.Field()
max_torque = scrapy.Field()
fuel_tank = scrapy.Field()
top_speed = scrapy.Field()
abs_ = scrapy.Field()
airbag_driver = scrapy.Field()
airbag_side = scrapy.Field()
alloy_wheels = scrapy.Field()
wheelbase = scrapy.Field()
central_locking = scrapy.Field()
parking_sensors = scrapy.Field()
reverse_camera = scrapy.Field()
maintanence = scrapy.Field()
general_warranty = scrapy.Field()
chassis_warranty = scrapy.Field()
"""
        

