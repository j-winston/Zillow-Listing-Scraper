import re
import requests
from bs4 import BeautifulSoup
from config import ZILLOW_URL

# TODO 1--Create lists of prices, addresses, and links from zillow.com

r = requests.get(url=ZILLOW_URL, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(r.content, 'lxml')

listing_links = soup.find_all(class_='list-card-link')
listing_addresses = soup.find_all('address', attrs={'class': 'list-card-addr'})
listing_prices = soup.find_all('div', attrs={'class': 'list-card-price'})

links = []
for link in listing_links:
    url_text = link.get('href')
    try:
        formatted_url = "http://www.zillow.com" + url_text
    except TypeError:
        pass
    else:
        links.append(formatted_url)

addresses = []
for address in listing_addresses:
    address_text = address.get_text()
    addresses.append(address_text)

prices = []
pattern = r"\+|/"
for price in listing_prices:
    price_text = price.getText()
    price_formatted = re.split(pattern, price_text)[0]
    prices.append(price_formatted)


