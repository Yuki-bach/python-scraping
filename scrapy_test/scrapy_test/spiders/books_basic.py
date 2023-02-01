import scrapy


class BooksBasicSpider(scrapy.Spider):
    name = 'books_basic'
    allowed_domains = ['quickwork.jp/']
    start_urls = ['https://quickwork.jp/news/']

    def parse(self, response):
        newss = response.xpath('/html/body/main/section[2]/div/div/a')
        for news in newss:
            yield {
                'date': news.xpath('.//p[2]/text()').get(),
                'title': news.xpath('.//p[3]/text()').get()
            }