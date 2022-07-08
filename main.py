import re
import time
import requests
import selenium.webdriver
from bs4 import BeautifulSoup
from config import ZILLOW_URL, GOOGLE_FORM_URL
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.common.by import By
<<<<<<< HEAD
from selenium.webdriver import ActionChains
=======
>>>>>>> old-state
import json

# Specify User-Agent to avoid captcha
r = requests.get(url=ZILLOW_URL, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'EN'})
soup = BeautifulSoup(r.content, 'lxml')

# Grab the entire chunk of javascript data
javascript_data = soup.find('script', attrs={'data-zrr-shared-data-key': "mobileSearchPageStore"})
javascript_text = javascript_data.getText()

# Get rid of extraneous symbols
clean_text = javascript_text.split('<!--')[1]
json_ready_text = clean_text.split('-->')[0]

# We are left with a nice neat JSON object with all the listing data
json_object = json.loads(json_ready_text)

# Extract the 40 listings from json object
json_filtered = json_object['cat1']['searchResults']['listResults']

zillow_links = []
zillow_addresses = []
zillow_prices = []
for zillow_listing in json_filtered:
    # Clean the formatting for abbreviated URLs
    url = zillow_listing['detailUrl']
    cleaned_url = re.sub("^/b", "http://www.zillow.com/b", url)
    url = ''.join(cleaned_url)

    # Rental price is tucked away in different places
    # we should gracefully handle this
    try:
        price = zillow_listing['price']
    except KeyError:
        price = zillow_listing['units'][0]['price']

    # Remove extraneous characters from price
    clean_price = re.split(r"\+|/", price)[0]
    price = clean_price

    address = zillow_listing['address']

    zillow_links.append(url)
    zillow_addresses.append(address)
    zillow_prices.append(price)

service = ChromeService(executable_path=ChromeDriverManager().install())
chrome_options = selenium.webdriver.chrome.options.Options()

# Detach option keeps browser window open
chrome_options.add_experimental_option('detach', True)

driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(url=ZILLOW_URL)
o = webdriver.ChromeOptions()


o.add_argument('user-data-dir=/home/james/.config/google-chrome/Default')
attempts = 0
while attempts < 10:
    captcha = driver.find_element(By.ID, 'px-captcha')
    action = ActionChains(driver)
    action.click_and_hold(captcha).perform()
    time.sleep(10)
    action.release(captcha).perform()
    time.sleep(.2)
    action.release(captcha)
    attempts += 1




# TODO--2.Consolidate this to one loop
# Get links to rentals

photo_cards = driver.find_elements(By.TAG_NAME, 'li')
for card in photo_cards:
    print(card)

# links = []
# for link in listing_links:
#     url_text = link.get('href')
#     try:
#         formatted_url = "http://www.zillow.com" + url_text
#     except TypeError:
#         pass
#     else:
#         links.append(formatted_url)
#
# # Get addresses for rentals
# addresses = []
# for address in listing_addresses:
#     address_text = address.get_text()
#     addresses.append(address_text)

# Get prices for rentals
# prices = []
# # Regex pattern for splitting prices $xxxx/m format
# pattern = r"\+|/"
# for price in listing_prices:
#     price_text = price.getText()
#     price_formatted = re.split(pattern, price_text)[0]
#     prices.append(price_formatted)


# Submit data to google form which will then automatically populate spreadsheet
driver.get(url=GOOGLE_FORM_URL)
for address, link, price in zip(zillow_addresses, zillow_links, zillow_prices):
    time.sleep(.5)
    address_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]'
                                                  '/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div'
                                                '/div/div[2]/div/div[1]/div/div[1]/input')
    link_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]'
                                               '/div/div[1]/div/div[1]/input')

    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    # Handle potential KeyErrors gracefully
    try:
        address_input.send_keys(address)
        price_input.send_keys(price)
        link_input.send_keys(link)
        submit_button.click()
        driver.get(url=GOOGLE_FORM_URL)
    except KeyError:
        pass
<<<<<<< HEAD


=======
#
>>>>>>> old-state
