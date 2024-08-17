import os
import ssl
import time
import shutil
import requests
import threading
import urllib.request
from PIL import Image
from io import BytesIO
from selenium import webdriver
from urllib.parse import urlparse
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
        print(f"  Into => {img_path}")

def handle_product_options(driver, product_name):
    try:
        # Wait for at least one image to be present
        WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.image-viewer-hero-container .gallery-item picture img')))

        # Get image elements
        image_elements = driver.find_elements(By.CSS_SELECTOR, '.image-viewer-hero-container .gallery-item picture img')

    except Exception as e:
        print(f"Error img ele ---------------------- : {e}")


    # Create a directory for the product images
    save_dir = os.path.join(os.getcwd(), "Images/Dick/2", product_name)
    os.makedirs(save_dir, exist_ok=True)

    # Download each image
    for i, image_element in enumerate(image_elements):
        # img_element = image_element.find_element_by_tag_name("img")
        image_url = image_element.get_attribute("src")
        if image_url is not None:
            img_url = image_url.split('?')[0]
            print(f'+ Downloading img {i}: ', img_url)
            download_image(img_url, save_dir)
        else: 
            print(f'- Img {i} None cmnr: ', image_url)
        time.sleep(2)  # delay for 5 seconds


    print(f"Finished download processing {product_name}")
    print('......................................................................... \n\n')


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
    
    time.sleep(10)

    product_options = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#pdp-color-attributes .sliding-row-outer .swatch-wrapper button')))

    product_options_len = len(product_options)
    if (product_options_len > 1):
        try:
            for i in range(0, product_options_len):
                target = f'#pdp-color-attributes .sliding-row-outer .swatch-wrapper:nth-of-type({i + 1}) button'
                product_target = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, target)))
                print(target)
                product_target.click()
                time.sleep(10)
                
                try:
                    product_name_p = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1[itemprop="name"]'))).text.strip()
                    product_color_p = driver.find_element(By.CSS_SELECTOR, '#pdp-color-attributes pdp-attribute-label-v2 span.hmf-header-xs').text.strip().replace("/", "-")
                    product_name = product_name_p + f"(Color {product_color_p})"
                except Exception as e:
                    print(f"Error product name: {e}")
                
                handle_product_options(driver, product_name)
        except Exception as e:
            print(f"Error product name handle: {e}")
        
            
    else:
        # You'll need to adjust the following lines based on the website structure
        try:
            product_name = driver.find_element(By.CSS_SELECTOR, 'h1[itemprop="name"]').text.strip()
        except Exception as e:
            print(f"Error product name: {e}")
        
        handle_product_options(driver, product_name)
    
    driver.quit()



with open('./Input/Dick/Dick20240812-2.txt', 'r') as f:
    urls = f.readlines()

with ThreadPoolExecutor(max_workers=3) as executor:
    for i, url in enumerate([url.strip() for url in urls]):
        executor.submit(process_url, url, i)