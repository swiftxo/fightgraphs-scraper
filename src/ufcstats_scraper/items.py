# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UfcstatsScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class EventItem(scrapy.Item):
    event_name = scrapy.Field()
    event_ufcstats_url = scrapy.Field()
    event_date = scrapy.Field()
    event_location = scrapy.Field()
    event_status = scrapy.Field()
    fight_refs = scrapy.Field()
