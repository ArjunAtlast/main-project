# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import CrawlSpider

class CarsItem(scrapy.Item):

    brand = scrapy.Field()
    model = scrapy.Field()
    generation = scrapy.Field()
    modification = scrapy.Field() #modification
    doors = scrapy.Field()
    power = scrapy.Field()
    fuel_tank_volume = scrapy.Field()
    coupe_type = scrapy.Field()
    seats = scrapy.Field()
    wheelbase = scrapy.Field()
    # trunk_volume = scrapy.Field() #minimum_volume_of_luggage
    torque = scrapy.Field()
    position_of_cylinders = scrapy.Field()
    number_of_cylinders = scrapy.Field()
    cylinder_bore = scrapy.Field()
    piston_stroke = scrapy.Field()
    compression_ratio = scrapy.Field()
    number_of_valves_per_cylinder = scrapy.Field() # number_of_valves_per_cylinder
    fuel_type = scrapy.Field()
    number_of_gears = scrapy.Field()
    abs = scrapy.Field()
    minimum_turning_circle = scrapy.Field()
    fuel_consumption_combined = scrapy.Field()
    kerb_weight = scrapy.Field()

class AutoSpider(CrawlSpider):
    name = 'auto'
    allowed_domains = ['www.auto-data.net']
    start_urls = ['http://www.auto-data.net/en/']
    
    def parse(self, response):
        """
        Parse starting page
        """

        brand_urls = response.css(".marki_blok::attr(href)").extract()

        for url in brand_urls:
            #create absolute url
            abs_url = response.urljoin(url)

            #request the url and parse it
            yield scrapy.Request(abs_url, callback=self.parse_brand)
            

    def parse_brand(self, response):
        """
        Parse each brand page
        """
        print('Processing..' + response.url)

        #get model links
        m_links = response.css(".modeli::attr(href)").extract()

        for link in m_links:

            #create absolute url
            abs_link = response.urljoin(link)

            #request and parse
            yield scrapy.Request(abs_link, callback=self.parse_model)

    def parse_model(self, response):
        """
        Parse each model page
        """
        print("Processing...", response.url)

        #get type links
        t_links = response.css("table.carData a::attr(href)").extract()

        for link in t_links:

            #create absolute url
            abs_link = response.urljoin(link)

            #request and parse
            yield scrapy.Request(abs_link, callback=self.parse_type)

    def parse_type(self, response):
        """
        Parse each type page
        """
        print("Processing...", response.url)

        #get data
        keys = response.css(".carData tr td:first-child::text").extract()
        vals = response.css(".carData tr td strong::text").extract()

        #closure function for filtering empty string from vals
        def filter_blank(text):
            if (text.strip()):
                return True
            else:
                return False
        # closure function ends

        #filter vals
        vals = list(filter(filter_blank, vals))
        # keys = list(filter(filter_blank, keys))

        #create a new empty dictionary to save data
        details = {}

        for i in range(0,len(keys)):

            #pre-process key
            key = self.preprocess_key(keys[i])

            #save data to corresponding key
            details[key] = vals[i].strip()
        
        # #save data as item
        yield self.create_item(details)
        
    def preprocess_key(self, key):
        """
        Preprocess the key
        """
        
        #strip whitespace and convert to lower case
        temp = key.strip().lower()

        #remove item in brackets
        temp = re.sub("\([^\)]*\)","",temp)

        #remove special characters and whitespaces
        temp = re.sub("[^a-z0-9]+","_", temp)

        #remove trailing '_' if any
        temp = re.sub("_$","",temp)

        return temp
    
    def create_item(self, details):
        """
        Create item from details parsed
        """

        #create a new Item instance
        item = CarsItem()

        for key in item.fields.keys():

            if key in details:
                item[key] = details[key]
            else:
                item[key] = 'NULL'

        # item['brand'] = details['brand']
        # item['model'] = details['model']
        # item['generation'] = details['generation']
        # item['modification'] = details['modification']
        # item['doors'] = details['doors']
        # item['power'] = details['power']
        # item['fuel_tank_volume'] = details['fuel_tank_volume']
        # item['coupe_type'] = details['coupe_type']
        # item['seats'] = details['seats']
        # item['wheelbase'] = details['wheelbase']
        # # item['trunk_volume'] = scrapy.Field() #minimum_volume_of_luggage
        # item['torque'] = details['torque']
        # item['position_of_cylinders'] = details['position_of_cylinders']
        # item['number_of_cylinders'] = details['number_of_cylinders']
        # item['cylinder_bore'] = details['cylinder_bore']
        # item['piston_stroke'] = details['piston_stroke']
        # item['compression_ratio'] = details['compression_ratio']
        # item['number_of_valves_per_cylinder'] = details['number_of_valves_per_cylinder'] # number_of_valves_per_cylinder
        # item['fuel_type'] = details['fuel_type']
        # item['number_of_gears'] = details['number_of_gears']
        # item['abs'] = details['abs']
        # item['minimum_turning_circle'] = details['minimum_turning_circle']
        # item['fuel_consumption_combined'] = details['fuel_consumption_combined']
        # item['kerb_weight'] = details['kerb_weight']

        return item


        


