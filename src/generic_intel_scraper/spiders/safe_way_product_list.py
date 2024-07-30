from typing import Iterable
import scrapy
from generic_intel_scraper.utils.get_headers import get_headers
from scrapy.spiders.init import InitSpider
from generic_intel_scraper.http.safeway_request_header import headers


class SafeWayProductListSpider(scrapy.Spider):
    name = 'safe_way_product_list'
    url_list = [
        "https://www.safeway.com/shop/product-details.970012939.html"
    ]

    def start_requests(self):
        for url in self.url_list:
            req = scrapy.Request(url,
                                 headers=headers, callback=self.parse, meta={'playwright': True})
            yield req

    def parse(self, response):
        product_name = response.css(
            'h1.product-details__product-title__text::text').get()
        yield {
            'product_name': product_name
        }
