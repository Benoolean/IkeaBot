import scrapy


class IkeaSpider(scrapy.Spider):
    name = "ikea_spider"
    def start_request(self):

        start_urls = ['https://www.ikea.com/ca/en/cat/grills-24898/?page=2']

        for urls in start_urls:
            yield scrapy.Response(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = 'ikea-%s.html' % page
        with open(filename, 'x') as f:
            f.write(response.body)
        
        self.log('Saved file %s' % filename)
        # for title in response.css('.post-header>h2'):
        #     yield {'title': title.css('a ::text').get()}

        # for next_page in response.css('a.next-posts-link'):
        #     yield response.follow(next_page, self.parse)