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
from PIL import Image
from io import BytesIO
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def download_image(url, save_dir, file_format='webp'):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        # Parse the URL to get the image name
        a = urlparse(url)
        img_name = os.path.basename(a.path)

        # Open the image with PIL
        img = Image.open(BytesIO(r.content))

        # Change the file extension to the desired format
        img_name = os.path.splitext(img_name)[0] + '.' + file_format.lower()

        # Join the save directory path with the image name
        img_path = os.path.join(save_dir, img_name)

        # Save the image in the desired format
        img.save(img_path, file_format.upper())
        print(f"Done______________{img_path}")


def process_url(url, index):
    driver = webdriver.Chrome()  # or whichever browser you prefer

    # Get screen size
    screen_width = driver.execute_script("return window.screen.availWidth")
    screen_height = driver.execute_script("return window.screen.availHeight")

    # Set window size and position
    quarter_screen_width = screen_width // 4
    driver.set_window_size(quarter_screen_width, 700)
    driver.set_window_position(quarter_screen_width * (index % 4), 0)

    driver.get(url)

    # driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, 'iframe-selector'))
    # # Wait for the button to be present
    # wait = WebDriverWait(driver, 10)
    # body = driver.find_element(By.TAG_NAME, 'body')
    # actions = ActionChains(driver)
    # actions.move_to_element_with_offset(body, 256, 350).click().perform()


    # button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button-selector')))


    # Wait for 10 seconds
    time.sleep(10)

    # You'll need to adjust the following lines based on the website structure
    try:
        product_name = driver.find_element(By.CSS_SELECTOR, 'h1[data-auid="PDP_ProductName"]').text.replace('?$pdp-gallery-ng$', '')
    except Exception as e:
        print(f"Error +++++++++++++++++++++++: {e}")

    try:
        # Wait for at least one image to be present
        WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.mobile-carousel .slick-slider .slick-list .slick-slide img')))

        # Get image elements
        image_elements = driver.find_elements(By.CSS_SELECTOR, '.mobile-carousel .slick-slider .slick-list .slick-slide img')

        print(image_elements[0])
    except Exception as e:
        print(f"Error +++++++++++++++++++++++++: {e}")


    # Create a directory for the product images
    save_dir = os.path.join(os.getcwd(), "Images/Academy/5", product_name)
    os.makedirs(save_dir, exist_ok=True)

    # Download each image
    for i, image_element in enumerate(image_elements):
        # img_element = image_element.find_element_by_tag_name("img")
        image_url = image_element.get_attribute("src")
        download_image(image_url, save_dir)
        print(f'Downloading img {i}: ', image_url)
        time.sleep(5)  # delay for 5 seconds


    print(f"Finished processing {product_name}")
    print('............................. \n\n')
    driver.quit()


with open('Academy5.txt', 'r') as f:
    urls = f.readlines()

with ThreadPoolExecutor(max_workers=3) as executor:
    for i, url in enumerate([url.strip() for url in urls]):
        executor.submit(process_url, url, i)