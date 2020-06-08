import scrapy


class IkeaSpider(scrapy.Spider):
    name = "ikea_spider"
    start_urls = ['https://www.ikea.com/ca/en/cat/products-products/']

    def parse(self, response):
        for title in response.css('.post-header>h2'):
            yield {'title': title.css('a ::text').get()}

        for next_page in response.css('a.next-posts-link'):
            yield response.follow(next_page, self.parse)