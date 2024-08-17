import os
import time
import threading
from selenium import webdriver
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.by import By
import ssl
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import os
import urllib.request
import ssl
import shutil
from urllib.parse import urlparse



def download_image(url, save_dir):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    r = requests.get(url, stream=True, headers=headers)
    if r.status_code == 200:
        # Parse the URL to get the image name
        a = urlparse(url)
        img_name = os.path.basename(a.path)

        # Join the save directory path with the image name
        img_path = os.path.join(save_dir, img_name)

        with open(img_path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
            print(f"Downloaded image to {img_path}")
    else:
        print(f"Failed to download image from {url}. Status code: {r.status_code}")


def process_url(url, index):
    driver = webdriver.Chrome()  # or whichever browser you prefer

    # Get screen size
    screen_width = driver.execute_script("return window.screen.availWidth")
    screen_height = driver.execute_script("return window.screen.availHeight")

    # Set window size and position
    quarter_screen_width = screen_width // 4
    driver.set_window_size(300, 700)
    driver.set_window_position(400 * index, 0)

    driver.get(url)

    # Click on the us-link link
    driver.find_element(By.CSS_SELECTOR, 'a.us-link').click()

    # Wait for 6 seconds
    time.sleep(6)

    # You'll need to adjust the following lines based on the website structure
    try:
        product_name = driver.find_element(By.CSS_SELECTOR, 'h1.heading-5').text
    except Exception as e:
        print(f"Error getting product name: {e}")

    try:
        # Wait for at least one image to be present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.media-gallery-base-content .seo-list li a img')))

        # Get image elements
        image_elements = driver.find_elements(By.CSS_SELECTOR, '.media-gallery-base-content .seo-list li a')
    except Exception as e:
        print(f"Error getting product name: {e}")


    # Create a directory for the product images
    save_dir = os.path.join(os.getcwd(), "Images/Bestbuy/6", product_name)
    os.makedirs(save_dir, exist_ok=True)

    # Download each image
    for i, image_element in enumerate(image_elements):
        print('Downloading image: ', i)
        image_url = image_element.get_attribute("href")
        download_image(image_url, save_dir)
        print('Downloaded image: ', image_url)

    print(f"Finished processing {product_name}")
    print('............................. \n\n')
    driver.quit()

    time.sleep(5)  # delay for 5 seconds

with open('Bestbuy6.txt', 'r') as f:
    urls = f.readlines()

with ThreadPoolExecutor(max_workers=3) as executor:
    for i, url in enumerate([url.strip() for url in urls]):
        executor.submit(process_url, url, i)