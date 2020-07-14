import scrapy
import os
import logging
import pandas as pd
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
        ikea_category_df_schema_data = {
            'category-id': [],
            'category_url': ''
        }
        
        ikea_category_df = pd.DataFrame(data=ikea_category_df_schema_data, dtype=str)
        category_list = enumerate(response.css('.vn-accordion__item > ul > li > a::attr(href)').getall())

        for index, category_url in category_list:
            # Getting the last array element in the stripped URL
            # .strip('/') removes the trailing / in the URL
            category_id = category_url.strip('/').split('-')[-1]
            ikea_category_df.loc[index] = [category_id, category_url]
        
        print(ikea_category_df)
        ikea_category_df.to_csv(categories_csv, encoding='utf-8', index=False)

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
    # yield runner.crawl(IkeaProductsSpider)
    reactor.stop()

crawl()
reactor.run() # the script will block here until the last crawl call is finished

# Executed after spiders are done crawling
