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
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import re
import pillow_avif


num = 1
dateTime = 'Lesliespool20240620'

def download_image(url, index, save_dir, file_format='avif'):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    r = requests.get(url, headers=headers)
    fileType = url.split('.')[-1]

    if r.status_code == 200:
        a = urlparse(url)
        imgName = os.path.basename(a.path)
        img_name = f'{imgName}-{index+1}.avif'
        
        img = Image.open(BytesIO(r.content))
        

        img_path = os.path.join(save_dir, img_name)
        
        img.save(img_path, file_format.upper())
        print(f"Done______________{img_path}")
    else:
        print(f"Error downloading image: {r.status_code}")

userAgent = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 11_15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6312.207 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6275.197 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6304.198 Safari/537.36']
def process_url(url, index):
    options = Options()
    
    options.add_argument('--headless=new') # for Chrome >= 109
    
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option("useAutomationExtension", False) 
    

    s = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=s, options=options)
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": userAgent[index % 4]}) 
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 

    screen_width = driver.execute_script("return window.screen.availWidth")
    screen_height = driver.execute_script("return window.screen.availHeight")

    quarter_screen_width = screen_width // 4
    driver.set_window_size(300, 700)
    driver.set_window_position(300 * (index % 4), 0)

    driver.get(url)

    try:
        product_name = driver.find_element(By.CSS_SELECTOR, 'h1.product-name').text.replace('/', '-')
    except Exception as e:
        print(f"Error getting product name: {e}")


    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.primary-images .slick-list .slick-slide picture source[media="(min-width: 1200px)"]')))

        image_elements = driver.find_elements(By.CSS_SELECTOR, 'div.primary-images .slick-list .slick-slide picture source[media="(min-width: 1200px)"]')
        
    except Exception as e:
        print(f"Error getting product name: {e}")


    save_dir = os.path.join(os.getcwd(), f'Images/Lesliespool/{dateTime}/{num}', product_name)
    os.makedirs(save_dir, exist_ok=True)

    for i, image_element in enumerate(image_elements):
        print('Downloading image: ', i)
        image_url = image_element.get_attribute("srcset")
        imgTarget = image_url.split(',')[1].strip().split(' ')[0]
        imgURL = imgTarget.split('?')[0]
        download_image(imgURL, i, save_dir)

    print(f"Finished processing {product_name}")
    print('............................. \n\n')
    driver.quit()

    time.sleep(5)  # delay for 5 seconds

with open(f'./Input/{dateTime}/Lesliespool{num}.txt', 'r') as f:
    urls = f.readlines()

with ThreadPoolExecutor(max_workers=4) as executor:
    for i, url in enumerate([url.strip() for url in urls]):
        executor.submit(process_url, url, i)
        # if i != 0 and (i+1) % 4 == 0:
        #     time.sleep(90)

