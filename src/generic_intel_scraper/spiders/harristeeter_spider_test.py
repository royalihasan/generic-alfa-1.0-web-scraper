import scrapy
import json
from typing import List, Dict, Any, Generator ,AsyncGenerator

import scrapy.http
from generic_intel_scraper.items.harris_teeter_items import HarrisTeeterItems
from generic_intel_scraper.utils.covert_yaml import yaml_to_selector
from generic_intel_scraper.utils.cookie_parser import parse_cookie
from scrapy import Selector

class HarrisTeeterSpider(scrapy.Spider):
    name = 'harris_teeter_test'
    allowed_domains = ['harristeeter.com']
    urls_list: List[str] = [
        'https://www.harristeeter.com/pl/chicken/05002?pzn=relevance'
    ]
    base_url: str = 'https://www.harristeeter.com'
    headers: Dict[str, str] = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8',
        'cache-control': 'no-cache',
        'device-memory': '8',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }

    custom_settings: Dict[str, Any] = {
        'DOWNLOAD_DELAY': 3,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 8,
        'CONCURRENT_REQUESTS': 1,
        'ITEM_PIPELINES': {
            'generic_intel_scraper.pipelines.rich_logging_pipeline.RichLoggingPipeline': 300,
        },
        'PLAYWRIGHT_BROWSER_TYPE': 'chromium',
    }

    def __init__(self):
        super().__init__()
        self.yaml_me = yaml_to_selector('harristeeter_pages_selector')

    def start_requests(self) -> Generator[scrapy.Request, None, None]:
        for url in self.urls_list:
            yield scrapy.Request(url=url, callback=self.parse_product_urls, meta={'playwright': True, 'playwright_include_page': True})

    async def parse_product_urls(self, response: scrapy.http.Response) :
        page = response.meta['playwright_page']
        cookies = parse_cookie(response)
        self.logger.info(json.dumps(cookies, indent=2))
        self.logger.info(f"URL: {response.url}")
        self.logger.info(f'RESPONSE {response.url}')

        while True:
            # Click the "Load More" button to load additional products, if present
            load_more_button = await page.query_selector('button.kds-Button.interactive.palette-accent.kind-prominent.variant-border.my-12.px-32.LoadMore__load-more-button')
            if load_more_button:
                await load_more_button.click()
                await page.wait_for_selector('a.kds-Link.kds-Link--inherit.kds-Link--implied.ProductDescription-truncated.overflow-hidden.text-primary')
                await page.wait_for_timeout(2000)  # Adjust timeout as needed
            else:
                break

        html = await page.content()
        s = Selector(text=html)
        await page.close()

        # Extract product URLs from the page
        urls_elements = s.css(
            'a.kds-Link.kds-Link--inherit.kds-Link--implied.ProductDescription-truncated.overflow-hidden.text-primary')
        urls = urls_elements.css('::attr(href)').getall()
        self.logger.info(f'Found URLs: {urls}')
        if not urls:
            self.logger.error('No URLs found on the page.')
            return
        print('Total Links:', len(urls))
        # Send requests for each product URL
        for product_url in urls:
            yield scrapy.Request(url=self.base_url + product_url, headers=self.headers, callback=self.parse_product)

    def parse_product(self, response: scrapy.http.Response) :
        self.logger.info(f'Parsing product page: {response.url}')
        script_data = response.css('#content > div > div > script::text').get()
        if script_data:
            try:
                product_data = json.loads(script_data)
                items = HarrisTeeterItems(
                    url=product_data.get('url'),
                    name=product_data.get('name'),
                    image=product_data.get('image'),
                    description=product_data.get('description'),
                    brand=product_data.get('brand'),
                    offers=product_data.get('offers'),
                    weight=response.css(self.yaml_me['weight']).get(),
                    rating=response.css(self.yaml_me['rating']).get(),
                    total_reviews=response.css(
                        self.yaml_me['total_reviews']).get(),
                    sku=product_data.get('sku'),
                    stocks=response.css(self.yaml_me['stocks']).get(),
                    sold_and_shipped_by=response.css(
                        self.yaml_me['sold_and_shipped_by']).get(),
                    sub_category=response.css(
                        self.yaml_me['sub_category']).getall()[1:3],
                )
                yield items
            except json.JSONDecodeError:
                self.logger.error('Failed to decode JSON from script tag.')
