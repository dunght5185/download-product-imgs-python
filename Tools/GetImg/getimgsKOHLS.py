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


    # You'll need to adjust the following lines based on the website structure
    try:
        product_name = driver.find_element(By.CSS_SELECTOR, 'h1.product-title').text
    except Exception as e:
        print(f"Error +++++++++++++++++++++++: {e}")

    try:
        # Wait for at least one image to be present
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.pdp-large-alt-images .large-alt-image img')))

        # Get image elements
        image_elements = driver.find_elements(By.CSS_SELECTOR, '.pdp-large-alt-images .large-alt-image img')
        image_elements2 = driver.find_elements(By.CSS_SELECTOR, '.pdp-large-hero-image img')

        print(image_elements[0])
    except Exception as e:
        print(f"Error +++++++++++++++++++++++++: {e}")


    # Create a directory for the product images
    save_dir = os.path.join(os.getcwd(), "Images/Kohls/1", product_name)
    os.makedirs(save_dir, exist_ok=True)

    # Download each image
    for i, image_element in enumerate(image_elements):
        # img_element = image_element.find_element_by_tag_name("img")
        image_url = image_element.get_attribute("src")
        download_image(image_url, save_dir)
        print(f'Downloading img {i}: ', image_url)
        time.sleep(1)  # delay for 5 seconds
    
    for j, image_element in enumerate(image_elements2):
        image_url = image_element.get_attribute("srcset")
        img_url = image_url.split(' ')[0]
        download_image(img_url, save_dir)
        print(f'Downloading img {j}: ', img_url)
        time.sleep(1)


    print(f"Finished processing {product_name}")
    print('............................. \n\n')
    driver.quit()


with open('kohls.txt', 'r') as f:
    urls = f.readlines()

with ThreadPoolExecutor(max_workers=3) as executor:
    for i, url in enumerate([url.strip() for url in urls]):
        executor.submit(process_url, url, i)