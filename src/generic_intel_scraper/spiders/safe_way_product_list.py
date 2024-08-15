import scrapy
from generic_intel_scraper.utils.cookie_parser import parse_cookie


class SafeWayProductListSpider(scrapy.Spider):
    name = 'safe_way_product_list'
    url_list = [
        "https://www.safeway.com/shop/product-details.960196388.html"
    ]
    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "COOKIES_ENABLED": True,
        "AUTOTHROTTLE_ENABLED": True,
        "CONCURRENT_REQUESTS": 5,
        "ROBOTSTXT_OBEY": False,
        "COOKIES_DEBUG": True,

        'PLAYWRIGHT_BROWSER_TYPE': 'chromium',
    }

    def start_requests(self):

        for url in self.url_list:
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={'playwright': True, 'playwright_include_page': True}

            )

    def parse(self, response):
        cookies = parse_cookie(response)
        self.logger.info(cookies)
        self.logger.info(response.url)
        self.logger.info(response.text)

        yield scrapy.Request(
            url=response.url,
            callback=self.start_requests,
            cookies=cookies,

        )

    def parse_product(self, response):
        self.logger.info(response.url)
        self.logger.info(response.text)
        yield {
            'url': response.url
        }
