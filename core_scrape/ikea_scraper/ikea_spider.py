import scrapy
import os
import logging
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from csv import reader
from crawled_handler import removeDuplicates

categories_csv = 'crawled/ikea_categories.csv'
products_csv = 'crawled/ikea_products.csv'

class IkeaCategoriesSpider(scrapy.Spider):
    name = 'ikea_categories'

    def start_requests(self):
        scrape_urls = [
            'https://www.ikea.com/ca/en/cat/products-products/'
        ]

        for url in scrape_urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        # creating/overwriting the product list with the columns of both
        # the product and category files
        with open(products_csv, 'w') as f:
            f.write('category,product_url\n')
            f.close()

        with open(categories_csv, 'w') as f:
            f.write('category,category_id\n')
            f.close()

        # Appending the category list
        product_list = enumerate(response.css('.vn-accordion__item > ul > li > a::attr(href)').getall())
        with open(categories_csv, 'a') as f:
            for product in product_list:
                # since product is a tuple (list #, value), product[1] contains
                # the category URL
                
                category_url = product[1].strip('/').split('/')[-1]
                category_id = category_url.split('-')[-1]

                category_name = ' '.join(category_url.split('-')[:-1])

                f.write('{name},{id}\n'.format(name=category_name, id=category_id))


            f.close()

        print('[CONSOLE]: Crawled categories and exported CSV files')


class IkeaProductsSpider(scrapy.Spider):
    name = 'ikea_products'

    def start_requests(self):
        with open(categories_csv) as f:
            categories_csv_urls = reader(f)
            # skip the header
            header = next(categories_csv_urls)
            
            if header != None:
                for url in categories_csv_urls:
                    # url <list(str)> into str
                    url = url[0]
                    yield scrapy.Request(url=url, callback=self.parse)

            f.close()


    def parse(self, response):
        category = response.css('title::text').get().replace('- IKEA', '').replace(',', '|').strip()

        # Links of all the product with url argument
        product_list = response.css('.range-revamp-product-compact > a::attr(href)').getall()

        with open(products_csv, 'a', encoding="utf-8") as f:
            for url in product_list:
                f.write('{category},{url}\n'.format(category=category, url=url))

            f.close()
    
    print('[CONSOLE]: Crawled products and exported CSV files')

logging.disable(20) # 20 is infomation logging

runner = CrawlerRunner()
@defer.inlineCallbacks
def crawl():
    yield runner.crawl(IkeaCategoriesSpider)
    yield runner.crawl(IkeaProductsSpider)
    reactor.stop()

crawl()
reactor.run() # the script will block here until the last crawl call is finished

# Executed after spiders are done crawling
