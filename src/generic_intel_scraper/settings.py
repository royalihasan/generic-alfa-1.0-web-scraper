BOT_NAME = "generic_intel_scraper"

SPIDER_MODULES = ["generic_intel_scraper.spiders"]
NEWSPIDER_MODULE = "generic_intel_scraper.spiders"


# Obey robots.txt rules
ROBOTSTXT_OBEY = True

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Proxy settings
# DOWNLOADER_MIDDLEWARES = {
#     # ...
#     'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
#     'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
#     # ...
# }

# ROTATING_PROXY_LIST = [
#     "148.72.165.7:80",
#     "47.251.43.115:443",
#     "50.168.72.114:8080",
#     "50.171.122.30:21",
#     "50.218.57.67:22",
#     "50.168.72.118:25",
#     "50.218.57.65:53",
#     "50.207.199.82:3306",
#     "50.223.239.168:5432",
#     "50.174.7.154:6379"
# ]

# SCRAPEOPS SETTINGS

# SCRAPEOPS_API_KEY = '0f49b1a1-3a81-4846-9d5a-bc1d1ce85e9a'
# SCRAPEOPS_PROXY_ENABLED = True
# CONCURRENT_REQUESTS = 1

# DOWNLOADER_MIDDLEWARES = {
#     'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
# }

# Playwright settings

# settings.py

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": False

}

PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 100000
