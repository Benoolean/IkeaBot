import scrapy
import sys
import os
import requests
import json
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

assert len(sys.argv) > 1

product_url = sys.argv[1]   
assert(requests.get(product_url).status_code != 404)

path = os.path.dirname(os.path.realpath(sys.argv[0]))
class IkeaAllProductsSpider(scrapy.Spider):
    name = 'ikea_product'

    def start_requests(self):
        self.log('Crawling: %s' % product_url )
        yield scrapy.Request(url=product_url, callback=self.parse)

    def parse(self, response):

        # Getting Product Data
        product_id = response.css('.range-revamp-product-identifier__number::text').get().replace('.', '')
        product_name = response.css('.range-revamp-header-section__title--big::text').get()
        product_price = response.css('.range-revamp-price__integer::text').get() + '.' + response.css('.range-revamp-price__decimals::text').get()
        product_type = response.css('.range-revamp-header-section__description-text::text').get()
        product_image_url = response.css('.range-revamp-aspect-ratio-image__image::attr(src)').get()

        
        # Getting Image
        req = requests.get(product_image_url, stream=True)

        if (req.status_code != 404):
            filename = os.path.join(path, 'crawled/product_image.jpg')
            with open(filename, 'wb') as img_file:
                img_file.write(req.content)
            
            self.log('Image downloaded successfully!')
        else:
            raise Exception('product image URL raised 404 expection. URL endpoint not found.')
            
        # Exporting Product Data
        product_data = {
            'product_id': product_id,
            'product_name': product_name,
            'product_price': product_price,
            'product_type': product_type,
            'product_image_url': product_image_url
        }

        filename = os.path.join(path, 'crawled/product_data.json')
        with open(filename, 'w') as img_file:
                img_file.write(json.dumps(product_data))

        # # debug
        # self.log(product_name + ' ' + product_price + ' ' + product_type)
        # self.log(product_image_url)

        # !deprecated!
        # # check if product_ID exists in the XML lookup
        # req = requests.get('https://www.ikea.com/ca/en/iows/catalog/availability/{product_id}/'.format(product_id=product_id))
        # if (req.status_code != 404):
        #     with open(filename, 'w') as f:
        #         f.write(product_id)
        #         f.close()
            
        #     self.log('Saved file %s' % filename)
        
        # else:
        #     self.log('Product XML Lookup resulted in 404 Error. Scraping regularly.')


configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(IkeaAllProductsSpider)
    reactor.stop()

crawl()
reactor.run()
