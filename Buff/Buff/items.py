# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BuffItem(scrapy.Item):
    biglabel = scrapy.Field()
    biglabel_link = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    market_name = scrapy.Field()
    price = scrapy.Field()
    exterior_wear= scrapy.Field()
    quality= scrapy.Field()
    rarity = scrapy.Field()
    type= scrapy.Field()
    weapon_type = scrapy.Field()


