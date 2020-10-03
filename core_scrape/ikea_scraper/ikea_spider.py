import scrapy
import os
import logging
import pandas as pd
import urllib.request
import json 

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from csv import reader
from crawled_handler import removeDuplicates
from google.cloud import bigquery


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
        ikea_category_df_data = {
            'category_id': [],
            'category_name': []
        }
        
        category_list = enumerate(response.css('.vn-accordion__item > ul > li > a::attr(href)').getall())

        for index, category_url in category_list:
            # Getting the last array element in the stripped URL
            # .strip('/') removes the trailing / in the URL
            category_name_id = category_url.strip('/').split('/')[-1]
            category_name = ' '.join(category_name_id.split('-')[:-1]).title()
            category_id = category_name_id.split('-')[-1]

            ikea_category_df_data['category_id'] += [category_id]
            ikea_category_df_data['category_name'] += [category_name]

        ikea_category_df = pd.DataFrame(data=ikea_category_df_data, dtype=str)
        ikea_category_df.to_csv(categories_csv, encoding='utf-8', index=False)

        print('[CONSOLE]: Crawled categories and exported CSV files')

        # getting products

        for index, row in ikea_category_df.iterrows():
            product_search_url = 'https://sik.search.blue.cdtapps.com/ca/en/product-list-page/more-products?category={category_id}&start=0&end=99999999'
            product_search_url = product_search_url.format(category_id=row['category_id'])

            with urllib.request.urlopen(product_search_url) as req_data:
                data = json.loads(req_data.read().decode())
                df = pd.DataFrame.from_dict(data['moreProducts']['productWindow'])
                df.to_gbq('ikea.products', chunksize=None, if_exists='append')
                
                print('Updated BigQuery data. Cateogory: {category_name}'.format(category_name=row['category_name']))

logger = logging.getLogger()
logger.setLevel(logging.INFO)

runner = CrawlerRunner()
@defer.inlineCallbacks
def crawl():
    yield runner.crawl(IkeaCategoriesSpider)
    reactor.stop()

crawl()
reactor.run() # the script will block here until the last crawl call is finished

# Executed after spiders are done crawling
