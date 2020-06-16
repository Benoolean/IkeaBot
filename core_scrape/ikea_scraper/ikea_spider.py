import scrapy
import os
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

temp_url = []

class IkeaAllProductsSpider(scrapy.Spider):
    name = 'ikea_all_products'

    def start_requests(self):
        file_dir = 'crawled/ikea_products.txt'
        if (os.path.exists(file_dir)): 
            os.remove(file_dir)

        start_urls = [
            'https://www.ikea.com/ca/en/cat/products-products/',
        ]

        for url in start_urls:
            self.log('Crawling: %s' % url )
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = 'crawled/ikea_all_products.txt'
        
        product_list = enumerate(response.css('.vn-accordion__item > ul > li > a::attr(href)').getall())

        with open(filename, 'w') as f:
            for index, product in product_list:
                f.write('{enum}|{url}\n'.format(enum=index+1, url=product))
                temp_url.append(product)

            f.close()
        
        self.log('Saved file %s' % filename)


class IkeaProductSpider(scrapy.Spider):
    name = 'ikea_product'

    def start_requests(self):
        start_urls = temp_url

        for url in start_urls:
            self.log('Crawling: %s' % url )
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.css('title::text').get()
        filename = 'crawled/ikea_products.txt'
        product_list = enumerate(response.css('.range-revamp-product-compact > a::attr(href)').getall())

        with open(filename, 'a') as f:
            f.write('URL|{page}\n'.format(page=page))
            for index, product in product_list:
                f.write('{url}\n'.format(url=product))

            f.write('\n')
            f.close()
        
        self.log('Saved file %s' % filename)

def migrateFile():
    file_dir = 'crawled/ikea_products.txt'
    if (os.path.exists(file_dir)): 
        if (os.path.exists('../../../../data/ikea_products.txt')):
            os.remove('../../../../data/ikea_products.txt')
            
        os.rename(file_dir, '../../../../data/ikea_products.txt')

configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(IkeaAllProductsSpider)
    yield runner.crawl(IkeaProductSpider)
    reactor.stop()

crawl()
reactor.run()
migrateFile()
