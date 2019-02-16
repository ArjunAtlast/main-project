# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


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
    maintenence = scrapy.Field()
    general_warranty = scrapy.Field()
    chassis_warranty = scrapy.Field()
    