import os
import time
import socks
import socket
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from urllib.request import urlretrieve

# Set up SOCKS5 proxy
socks.set_default_proxy(socks.SOCKS5, "192.241.112.175", 7677, True, "pnnolbtb", "d44vagcekzbp")
socket.socket = socks.socksocket

# Set up Chrome options
options = Options()
# options.add_argument('--headless')  # Run Chrome in headless mode

# Initialize the Chrome driver with the specified options
driver = webdriver.Chrome(service=Service('/usr/local/bin/chromedriver'), options=options)

# Read the URLs from the text file
with open('/Input/Lowes.txt', 'r') as file:
    urls = file.read().splitlines()

for url in urls:
    try:
        driver.get(url)

        # Wait for 20 seconds for the page to load
        time.sleep(150)

        # Find the product name and image URL(s)
        product_name = driver.find_element_by_css_selector('h1').text
        img_urls = [img.get_attribute('src') for img in driver.find_elements_by_css_selector('img.tile-img')]

        # Create a new directory with the product name
        os.mkdir(product_name)
        print(f'Downloaded {product_name}')

        # Download each image and save it to the new directory
        for i, img_url in enumerate(img_urls):
            urlretrieve(img_url, os.path.join(product_name, f'image{i}.jpg'))
    except Exception as e:
        print(f"Error processing {url}: {e}")

        