# BOT_NAME = "generic_intel_scraper"

SPIDER_MODULES = ["generic_intel_scraper.spiders"]
NEWSPIDER_MODULE = "generic_intel_scraper.spiders"

# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# SCRAPEOPS SETTINGS

SCRAPEOPS_API_KEY = '2b1b732f-ce34-4a84-87a1-8d3955aaa013'
SCRAPEOPS_PROXY_ENABLED = True
# SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True
# CONCURRENT_REQUESTS = 1

DOWNLOADER_MIDDLEWARES = {
    # 'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sd?k.ScrapeOpsScrapyProxySdk': 725,
    # 'generic_intel_scraper.middlewares.scrape_ops_user_agents.ScrapeOpsFakeUserAgentMiddleware': 400,

}


#  Playwright settings

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": False,

}

PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 5000000
# PLAYWRIGHT_PROCESS_REQUEST_HEADERS = None
# PLAYWRIGHT_BROWSER_TYPE = "firefox"
