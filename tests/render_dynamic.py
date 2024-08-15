import requests
from requests_html import HTMLSession
url = 'https://www.harristeeter.com/pl/computers-laptops-tablets/29004?pzn=relevance'

s = HTMLSession()
r = s.get(url)
r.html.find('a.kds-Link.kds-Link--inherit.kds-Link--implied.ProductDescription-truncated.overflow-hidden.text-primary')

# print(r.status_code)
