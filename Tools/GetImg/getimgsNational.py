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
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import os
import urllib.request
import ssl
import shutil
from PIL import Image
from io import BytesIO
from urllib.parse import urlparse




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
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')


    driver = webdriver.Chrome()
    # Get screen size
    # screen_width = driver.execute_script("return window.screen.availWidth")
    # screen_height = driver.execute_script("return window.screen.availHeight")

    # Set window size and position
    # quarter_screen_width = screen_width // 4
    driver.set_window_size(1440, 816)
    driver.set_window_position(0 , 0)

    driver.get(url)

    try:
        # Wait for the cookie consent popup to load
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ctct-popup-wrapper.ctct-popup-is-visible .ctct-popup-content')))

        # Click the "Accept" button
        driver.find_element(By.CSS_SELECTOR, '.ctct-popup-wrapper.ctct-popup-is-visible .ctct-popup-content .ctct-popup-content button.ctct-popup-close').click()
    except Exception as e:
        print(f"Error accepting cookies: {e}")

    # You'll need to adjust the following lines based on the website structure
    try:
        product_name = driver.find_element(By.CSS_SELECTOR, 'h1.productView-title.main-heading').text.replace('/', '-')
    except Exception as e:
        print(f"Error getting product name: {e}")


    try:
        # Wait for at least one image to be present
        # WebDriverWait(driver, 2000).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section.productView-images .slick-list .slick-track .productView-thumbnail')))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section.productView-images ul.productView-thumbnails li.productView-thumbnail')))
        # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fotorama-item .fotorama__stage .fotorama__stage__frame')))
        # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.product-info-main-wrapper .product.media ._block-content-loading')))


        # Get image elements
        image_elements = driver.find_elements(By.CSS_SELECTOR, 'section.productView-images ul.productView-thumbnails li.productView-thumbnail a')
        # image_elements = driver.find_elements(By.CSS_SELECTOR, 'section.productView-images .slick-list .slick-track .productView-thumbnail a')
        # image_elements = driver.find_elements(By.CSS_SELECTOR, '.fotorama-item .fotorama__stage .fotorama__stage__frame img')
        # image_elements = driver.find_elements(By.CSS_SELECTOR, '.product-info-main-wrapper .product.media ._block-content-loading img')

        print(image_elements[0])
    except Exception as e:
        print(f"Error getting product name: {e}")




    # Create a directory for the product images
    save_dir = os.path.join(os.getcwd(), "Images/Doheny/1", product_name)
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

with open('Input/Pool20240703/Nationaldiscountpoolsupplies1.txt', 'r') as f:
    urls = f.readlines()

with ThreadPoolExecutor(max_workers=3) as executor:
    for i, url in enumerate([url.strip() for url in urls]):
        executor.submit(process_url, url, i)
        time.sleep(10)