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
    r = requests.get(url, stream=True)
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

def download_image2(image_url, save_dir):
    file_path = os.path.join(save_dir, os.path.basename(image_url))
    print(f"Downloading image from {image_url} to {file_path}")
    try:
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)  # Use TLSv1.2
        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'),
            ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
            ('Accept-Language', 'en-US,en;q=0.5'),
            ('DNT', '1'),
            ('Connection', 'keep-alive'),
            ('Upgrade-Insecure-Requests', '1')
        ]
        urllib.request.install_opener(opener)
        response = urllib.request.urlopen(image_url, context=gcontext)
        with open(file_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Downloaded image to {file_path}")
    except Exception as e:
        print(f"Error downloading image: {e}")


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


    # You'll need to adjust the following lines based on the website structure
    try:
        product_name = driver.find_element(By.CSS_SELECTOR, 'h1.product-info__header_title').text
    except Exception as e:
        print(f"Error getting product name: {e}")

    try:
        # Wait for at least one image to be present
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.swiper-slide img.product-image__swiper_img')))

        # Get image elements
        image_elements = driver.find_elements(By.CSS_SELECTOR, '.swiper-slide img.product-image__swiper_img')

        print(image_elements[0])
    except Exception as e:
        print(f"Error getting product name: {e}")


    # Create a directory for the product images
    save_dir = os.path.join(os.getcwd(), "Images/Bounth", product_name)
    os.makedirs(save_dir, exist_ok=True)

    # Download each image
    for i, image_element in enumerate(image_elements):
        print('Downloading image: ', i)
        image_url = 'https:'+image_element.get_attribute("data-zoom-src")
        download_image(image_url, save_dir)
        print('Downloaded image: ', image_url)

    print(f"Finished processing {product_name}")
    print('............................. \n\n')
    driver.quit()

    time.sleep(5)  # delay for 5 seconds

with open('Bounth.txt', 'r') as f:
    urls = f.readlines()

with ThreadPoolExecutor(max_workers=3) as executor:
    for i, url in enumerate([url.strip() for url in urls]):
        executor.submit(process_url, url, i)