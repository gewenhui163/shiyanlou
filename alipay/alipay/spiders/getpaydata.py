# -*- coding: utf-8 -*-
import scrapy


class GetpaydataSpider(scrapy.Spider):
    name = 'getpaydata'

    start_urls = ['https://auth.alipay.com/login/index.html']

    def parse(self, response):
        csrf_token = response.xpath('//input[@name="rds_form_token"]/@value').extract_first()
        self.logger.info(csrf_token)
        print("==========>")
        print(csrf_token)
        print("<==========")

        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'rds_form_token': csrf_token,
                # 这里要改为自己的邮箱和密码
                'logonId': '13918421050',
                'password_rsainput': '',
            },
            callback=self.after_login
        )

    def after_login(self, response):
        return [scrapy.Request(
            url='https://my.alipay.com/portal/i.htm?referer=https%3A%2F%2Fauth.alipay.com%2Flogin%2Findex.htm',
            callback=self.parse_after_login
        )]

    def parse_after_login(self, response):
        return {
            'amount': response.xpath('//td[@class="amount"]/span/text()').extract()
        }