# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import RepositoryItem

class GithubPySpider(scrapy.Spider):
    name = 'github.py'
    #allowed_domains = ['github.com']

    @property
    def start_urls(self):
        urls = ('https://github.com/shiyanlou?tab=repositories',
                'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK0MjAxNy0wNi0wNlQyMjoyMToxMFrOBZKVZw%3D%3D&tab=repositories', \
                'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK0MjAxNS0wMS0yNlQwMzozMDoyNVrOAcdiUA%3D%3D&tab=repositories',
                'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK0MjAxNC0xMS0yMVQxMDowOTowMlrOAZ0AWQ%3D%3D&tab=repositories')

        return urls
    def parse(self, response):
        yield RepositoryItem({
            'name': response.xpath('//div[@id="user-repositories-list"]/ul/li/div[1]/div/h3/a/text()').re('[\s]*(\S+)[\s]*'),
            'update_time': response.xpath('//div[@id="user-repositories-list"]/ul/li/div[1]/div/relative-time/@datetime').extract()
        })
