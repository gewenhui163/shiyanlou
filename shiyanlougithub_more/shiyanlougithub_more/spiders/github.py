# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub_more.items import githubMoreItem

class GithubSpider(scrapy.Spider):
    name = 'github'
    #allowed_domains = ['github.com/shiyanlou']

    start_urls = ['https://github.com/shiyanlou?tab=repositories']

    def parse(self, response):
        for github in response.xpath('//div[@id="user-repositories-list"]/ul/li'):
            item = githubMoreItem()
            item['name'] = github.xpath('.//div[1]/div/h3/a/text()').re_first('[\s]*(\S+)[\s]*')
            item['update_time'] = github.xpath('.//div[1]/div/relative-time/@datetime').extract_first()

            github_url = 'https://github.com/shiyanlou/' + item['name']
            requset = scrapy.Request(github_url, callback=self.parse_github)
            requset.meta['item'] = item
            yield requset

            for url in response.xpath('//div[@class="paginate-container"]/div/a/@href'):
                print(url)
                yield response.follow(url, callback=self.parse)

    def parse_github(self, response):
        item = response.meta['item']
        item['commits'] = response.xpath('//ul[@class="numbers-summary"]/li[1]/a/span/text()').re_first('[\s]*(\d+)[\s]*')
        item['branches'] = response.xpath('//ul[@class="numbers-summary"]/li[2]/a/span/text()').re_first('[\s]*(\d+)[\s]*')
        item['releases'] = response.xpath('//ul[@class="numbers-summary"]/li[3]/a/span/text()').re_first('[\s]*(\d+)[\s]*')

        yield item





