import scrapy
import json


class HarrisTeeterSpider(scrapy.Spider):
    name = 'harris_teeter'
    allowed_domains = ['harristeeter.com']
    urls_list = [
        'https://www.harristeeter.com/pl/chicken/05002'
    ]
    headers = {
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
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }

    custom_settings = {
        'DOWNLOAD_DELAY': 10,
        'COOKIES_ENABLED': True,
        'COOKIES_DEBUG': True,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 8,
        'CONCURRENT_REQUESTS': 1,


    }

    def start_requests(self):
        for url in self.urls_list:
            yield scrapy.Request(url=url, callback=self.parse_initial, headers=self.headers, )

    def parse_initial(self, response):
       
        for url in self.urls_list:
            yield scrapy.Request(
                url=url,
                callback=self.parse_product,
                headers=self.headers,
                cookies=self.cookies_dict,
                meta={'playwright': True, 'playwright_include_page': True}
            )

    def parse_product(self, response):
        print('RESPONSE', response.url)
        # Extract and print URLs
        url = response.css(
            'a.kds-Link.kds-Link--inherit.kds-Link--implied.ProductDescription-truncated.overflow-hidden.text-primary::attr(href)').getall()
        print('URL', url)

        # Extract and print page title
        page_title = response.css('title::text').get()
        print('PAGE_TITLE', page_title)

        # Extract and parse script data if needed
        script_data = response.css('#content > div > div > script::text').get()
        if script_data:
            try:
                product_data = json.loads(script_data)
                yield {
                    'url': product_data.get('url'),
                    'name': product_data.get('name'),
                    'image': product_data.get('image'),
                    'description': product_data.get('description'),
                    'brand': product_data.get('brand', {}).get('name'),
                    'offers': product_data.get('offers'),
                    'weight': response.css('span.ProductDetails-sellBy::text').get(),
                    'rating': response.css('span.kds-Text--m.mx-4.text-accent-more-prominent::text').get(),
                    'sku': product_data.get('sku')
                }
            except json.JSONDecodeError:
                self.logger.error('Failed to decode JSON from script tag.')
