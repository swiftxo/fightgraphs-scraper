# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UfcstatsScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class FighterImageItem(scrapy.Item):
    fighter_ufcstats_url = scrapy.Field()
    fighter_image_url = scrapy.Field()


class EventItem(scrapy.Item):
    event_name = scrapy.Field()
    event_ufcstats_url = scrapy.Field()
    event_date = scrapy.Field()
    event_location = scrapy.Field()
    event_status = scrapy.Field()
    fight_refs = scrapy.Field()


class FighterItem(scrapy.Item):
    fighter_ufcstats_url = scrapy.Field()
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    nickname = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    reach = scrapy.Field()
    stance = scrapy.Field()
    fighter_record = scrapy.Field()
    date_of_birth = scrapy.Field()
    fight_urls = scrapy.Field()


class FightItem(scrapy.Item):
    fight_ufcstats_url = scrapy.Field()
    fight_details = scrapy.Field()
    fight_stats = scrapy.Field()
    fighter1 = scrapy.Field()
    fighter2 = scrapy.Field()
