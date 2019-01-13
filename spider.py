import json

from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

results = []

start_urls = ['https://www.shiyanlou.com/courses/427']

def parse(response):
    for comment in response.css('div.comment-list-item'):
        name = comment.xpath('.//div[@class="user-username"]/a/text()').re_first('[\s]*(\S+)[\s]*')
        content = comment.xpath('.//div[contains(@class, "comment-item-content")]/p/text()').extract_first()
        #print(name + '---' + content)
        result = dict(
            username = name,
            content = content
        )
        print(result)
        results.append(result)

def has_next_page(response):
    classes = response.xpath('//li[containes(@class,"next-page")]/@class').extract_first()
    return 'disabled' not in classes

def goto_next_page(driver):
    driver.find_element_by_xpath('//li[contains(@class,"next-page")]').click()
    pass

def wait_page_retrun(driver, page):
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, '//ul[@class="pagination"]/li[@class="active"]'),
            str(page)
        )
    )

def spider():
    driver = webdriver.PhantomJS()
    url = 'https://www.shiyanlou.com/courses/427'
    driver.get(url)
    page = 1
    while True:
        wait_page_retrun(driver, page)
        html = driver.page_source
        resposne = HtmlResponse(url=url, body=html.encode('utf8'))
        parse(resposne)
        print('====>')
        print(resposne.xpath('//li[containes(@class,"next-page")]/@class').extract_first())
        if not has_next_page(resposne):
            break
        page += 1
        goto_next_page(driver)

    with open('/home/gewenhui/Code/eviroment/Code/comments.json', 'w') as f:
        f.write(json.dumps(results))

if __name__ == '__main__':
    spider()