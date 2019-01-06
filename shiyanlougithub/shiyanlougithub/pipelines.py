# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from shiyanlougithub.models import Repository, engine
from datetime import datetime

class ShiyanlougithubPipeline(object):
    def process_item(self, item, spider):
        # print('======>000')
        # print(item)
        # print('<======000')
        item['name'] = item['name'][0]
        # if (isinstance(item['update_time'], list)):
        item['update_time'] = datetime.strptime(item['update_time'][0].split('T')[0], '%Y-%m-%d').date()
        # else:
        #     item['update_time'] = datetime.strptime(item['update_time'].split()[0], '%Y-%m-%d').date()
        self.session.add(Repository(**item))

    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()