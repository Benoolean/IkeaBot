import os
import sys
import json
import xmltodict
import request
from urllib.request import urlopen

assert len(sys.argv) > 1
product_url = sys.argv[1]

def importXML():
    xml_data = urlopen(product_url).read()

    with open('crawled/ikea_product.json', 'w') as json_file:
        json.dump(xmltodict.parse(xml_data), json_file)


importXML()

# configure_logging()
# runner = CrawlerRunner()

# # @defer.inlineCallbacks
# # def crawl():
# #     yield runner.crawl(IkeaProductSpider)
# #     reactor.stop()

# # crawl()
# # reactor.run()
