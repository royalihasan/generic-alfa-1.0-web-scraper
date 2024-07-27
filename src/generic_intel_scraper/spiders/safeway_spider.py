import scrapy
from generic_intel_scraper.items.safeway_items import SafewayItem
from generic_intel_scraper.utils.covert_yaml import yaml_to_selector


class SafewaySpider(scrapy.Spider):
    name = 'safeway'
    start_urls = [
        'https://www.safeway.com/shop/aisles/baby-care.html?loc=3132']

    def __init__(self):
        self.yaml_me = yaml_to_selector('safeway_page_selectors')

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={'playwright': True})

    def parse(self, response):
        category = response.css(self.yaml_me['product_category']).get()
        print("CATEGORY: ", category)
        # Extract product information
        for product in response.css('div.product-title'):
            title = product.css('a.product-title__name::text').get()
            details = product.css('div.product-title__qty span::text').getall()
            print("TITLE: ", title)
            print("DETAILS: ", details)

            # Join details into a single string
            details_text = ' '.join(details).strip()

            print("DETAILS TEXT: ", details_text)

            # Create a SafewayItem object
            item = SafewayItem()
            item['title'] = title
            item['details'] = details_text
            yield item
