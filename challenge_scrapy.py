#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import scrapy

class GithubSpider(scrapy.Spider):
    name = 'github-spider'

    @property
    def start_urls(self):
        #urls = ('https://github.com/shiyanlou?tab=repositories', 'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK0MjAxNy0wNi0wNlQyMjoyMToxMFrOBZKVZw%3D%3D&tab=repositories',\
                #'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK0MjAxNS0wMS0yNlQwMzozMDoyNVrOAcdiUA%3D%3D&tab=repositories', 'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK0MjAxNC0xMS0yMVQxMDowOTowMlrOAZ0AWQ%3D%3D&tab=repositories')

        urls = ['https://github.com/shiyanlou?tab=repositories']
        return urls

    def parse(self, response):
        for git in response.xpath('//div[@id="user-repositories-list"]/ul/li/div[1]'):
            print(git.xpath('.//div/h3/a/text()').re('[\s]*(\S+)[\s]*'))
            print(git.xpath('.//div/relative-time/@datetime').extract())
            yield {
                "name": git.xpath('.//div/h3/a/text()').re('[\s]*(\S+)[\s]*'),
                "update": git.xpath('.//div/relative-time/@datetime').extract()
                }
        #scrapy runspider scrapy.py -o shiyanlougithub.json