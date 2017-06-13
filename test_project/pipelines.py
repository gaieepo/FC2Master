# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import test_project.setting
import pymysql.cursors


class DBPipeline(object):
    # MYSQL_HOST = 'localhost'
    # MYSQL_DBNAME = 'crawler'
    # MYSQL_USER = 'root'
    # MYSQL_PASSWORD = ''
    def __init__(self, db):
        self.db = db

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf-8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        db = pymysql.connect(**dbparams)
        return cls(db)

    def process_item(self, item, spider):
        cursor = self.dbpool.cursor()
        sql = ""
        return item
