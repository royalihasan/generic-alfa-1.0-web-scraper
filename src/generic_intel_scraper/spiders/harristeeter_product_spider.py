import scrapy


class HarrisTeeterProductSpider(scrapy.Spider):
    name='harris_teeter_product'
    url = 'https://www.harristeeter.com/pl/chicken/05002'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        product_name = response.css('h1').getall()
        yield {
            'product_name': product_name
        }
