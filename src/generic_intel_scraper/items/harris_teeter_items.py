import scrapy


class HarrisTeeterItems(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    image = scrapy.Field()
    description = scrapy.Field()
    brand = scrapy.Field()
    offers = scrapy.Field()
    weight = scrapy.Field()
    rating = scrapy.Field()
    total_reviews = scrapy.Field()
    sku = scrapy.Field()
    stocks = scrapy.Field()
    sold_and_shipped_by = scrapy.Field()
    sub_category = scrapy.Field()
