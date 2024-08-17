import os
import time
import threading
from selenium import webdriver
import urllib.request
from concurrent.futures import ThreadPoolExecutor
import ssl
import requests
import shutil
from urllib.parse import urlparse
from PIL import Image
from io import BytesIO
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import warnings
from urllib3.exceptions import InsecureRequestWarning



def download_image(url, save_dir, file_format='webp'):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        a = urlparse(url)
        
        img_name = os.path.basename(a.path)
        warnings.filterwarnings("ignore", category=InsecureRequestWarning)
        img = Image.open(BytesIO(r.content))

        img_name = os.path.splitext(img_name)[0] + '.' + file_format.lower()

        img_path = os.path.join(save_dir, img_name)

        img.save(img_path, file_format.upper())
        print(f"Done______________{img_path}")


def process_url(url, index):
    driver = webdriver.Chrome() 

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
        product_name = driver.find_element(By.CSS_SELECTOR, 'h1').text
    except Exception as e:
        print(f"Error +++++++++++++++++++++++: {e}")

    try:
        # Wait for at least one image to be present
        WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'link[as="image"]')))

        # Get image elements
        image_elements = driver.find_elements(By.CSS_SELECTOR, 'link[as="image"]')

        print(image_elements[0])
    except Exception as e:
        print(f"Error +++++++++++++++++++++++++: {e}")


    # Create a directory for the product images
    save_dir = os.path.join(os.getcwd(), "Images/Sharper/20240806/2", product_name)
    os.makedirs(save_dir, exist_ok=True)

    # Download each image
    for i, image_element in enumerate(image_elements):
        # img_element = image_element.find_element_by_tag_name("img")
        image_url = image_element.get_attribute("href")
        download_image(image_url, save_dir)
        print(f'Downloading img {i}: ', image_url)
        time.sleep(5)  # delay for 5 seconds


    print(f"Finished processing {product_name}")
    print('............................. \n\n')
    driver.quit()


with open('./Input/Sharper/Sharper202408062.txt', 'r') as f:
    urls = f.readlines()

with ThreadPoolExecutor(max_workers=3) as executor:
    for i, url in enumerate([url.strip() for url in urls]):
        executor.submit(process_url, url, i)