import scrapy
from generic_intel_scraper.items.safeway_items import SafewayItem
from generic_intel_scraper.utils.covert_yaml import yaml_to_selector
from generic_intel_scraper.http.safeway_request_header import headers


class SafewaySpider(scrapy.Spider):
    name = 'safeway'
    start_urls = [
        'https://www.safeway.com/shop/aisles/baby-care.html?loc=3132']
    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "COOKIES_ENABLED": True,
        "AUTOTHROTTLE_ENABLED": True,
        "CONCURRENT_REQUESTS": 5,
        "ROBOTSTXT_OBEY": False,
        "COOKIES_DEBUG": True

    }

    def __init__(self):
        self.yaml_me = yaml_to_selector('safeway_page_selectors')

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, headers=headers, meta={'playwright': True})

    def parse(self, response):
        category = response.css(self.yaml_me['product_category']).get()
        print("CATEGORY: ", category)
        # Extract product information
        for product in response.css('div.product-title'):
            title = product.css(self.yaml_me['product_title']).get()
            details = product.css(self.yaml_me['product_details']).getall()
            link = product.css(self.yaml_me['product_links']).get()
            self.logger.info("PRODUCT LINK: %s", link)
            full_link = "https://www.safeway.com" + link

            yield scrapy.Request(full_link, callback=self.parse_product, headers=headers, meta={"playwright": True, "product_name": title, "product_details": details})

    def parse_product(self, response):
        product_name = response.css('h1[data-qa="pdp-prdctnm"]::text').get()
        print("PRODUCT NAME: ", product_name)
