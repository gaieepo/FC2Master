# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VideoItem(scrapy.Item):
    """ Video """
    vid = scrapy.Field()
    title = scrapy.Field()
    img_src = scrapy.Field()
    duration = scrapy.Field()
    permission = scrapy.Field()
    view_count = scrapy.Field()
    comment_count = scrapy.Field()
    star_count = scrapy.Field()
    user_id = scrapy.Field()


class UserItem(scrapy.Item):
    """ User """
    uid = scrapy.Field()
    name = scrapy.Field()
