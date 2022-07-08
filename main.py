import re
import time
import requests
import selenium.webdriver
from bs4 import BeautifulSoup
from config import ZILLOW_URL, GOOGLE_FORM_URL, GOOGLE_BACKEND_URL
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

# # TODO--1.Use selenium for this
service = ChromeService(executable_path=ChromeDriverManager().install())
chrome_options = selenium.webdriver.chrome.options.Options()
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


# ActionChains.click_and_hold()

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


# # Submit data to google form which automatically populates spreadsheet
# # Otherwise we'd have to use selenium webdriver with normal browser profile
# driver.get(url=GOOGLE_FORM_URL)
# for address, link, price in zip(addresses, links, prices):
#     time.sleep(1)
#     address_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]'
#                                                   '/div/div/div[2]/div/div[1]/div/div[1]/input')
#     price_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div'
#                                                 '/div/div[2]/div/div[1]/div/div[1]/input')
#     link_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]'
#                                                '/div/div[1]/div/div[1]/input')
#
#     submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
#     try:
#         address_input.send_keys(address)
#         price_input.send_keys(price)
#         link_input.send_keys(link)
#         submit_button.click()
#         driver.get(url='https://docs.google.com/forms/d/e/'
#                        '1FAIpQLSdWK_d496X6gXIonv9wB43LenjzSgsWobrFvmuS4m_Shk4QyQ/viewform')
#         driver.get(url=GOOGLE_FORM_URL)
#     except KeyError:
#         pass

