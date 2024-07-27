import scrapy

class SafewayItem(scrapy.Item):
    title=scrapy.Field()
    details=scrapy.Field()