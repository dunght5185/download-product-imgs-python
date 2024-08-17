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
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

inputFilePath = '../../Input/Homedeport/Homedeport-1.txt'
saveImgToFolder = '../../Images/Homedeport/20240817/1'

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
        img_path = os.path.join(save_dir, img_name).replace('/Tools/GetImg/../..','')

        # Save the image in the desired format
        img.save(img_path, file_format.upper())
        print(f"  Into => {img_path}")

def handle_product_options(driver, product_name):
    try:
        # Wait for at least one image to be present
        WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#media-gallery .mediagallery__thumbnail button img')))

        # Get image elements
        image_elements = driver.find_elements(By.CSS_SELECTOR, '#media-gallery .mediagallery__thumbnail button img')

    except Exception as e:
        print(f"Error img ele ---------------------- : {e}")


    # Create a directory for the product images
    save_dir = os.path.join(os.getcwd(), saveImgToFolder, product_name)
    os.makedirs(save_dir, exist_ok=True)

    # Download each image
    for i, image_element in enumerate(image_elements):
        # img_element = image_element.find_element_by_tag_name("img")
        image_url = image_element.get_attribute("src")
        if image_url is not None:
            img_first = image_url.split('_')[0]
            img_last = '_600.jpg'
            img_url = img_first + img_last
            print(f'+ Downloading img {i}: ', img_url)
            download_image(img_url, save_dir)
        else: 
            print(f'- Img {i} None cmnr: ', image_url)
        time.sleep(1)  # delay for 5 seconds


    print(f"Finished download processing {product_name}")
    print('......................................................................... \n\n')


def process_url(url, index):
    # driver = webdriver.Chrome()  # or whichever browser you prefer

    userAgent = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36']

    options = Options()
    # options.add_argument('--headless=new') # for Chrome >= 109
    
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option("useAutomationExtension", False) 
    
    s = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=s, options=options)
    # driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": userAgent[index % 3]}) 
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": userAgent[0]}) 
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
    

    # Get screen size
    screen_width = driver.execute_script("return window.screen.availWidth")
    screen_height = driver.execute_script("return window.screen.availHeight")
    
    # Set window size and position
    quarter_screen_width = screen_width // 3
    # driver.set_window_size(1280, 768)
    driver.set_window_size(quarter_screen_width, 700)
    driver.set_window_position(quarter_screen_width * (index % 3), 0)

    driver.get(url)
    
    time.sleep(5)
    
    try:
        product_name_pre = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.product-details__badge-title--wrapper h1'))).text.strip()
        product_name = product_name_pre.replace('/', '-')
    except Exception as e:
        print(f"Error product name: {e.message}")
    
    handle_product_options(driver, product_name)
    
    driver.quit()



with open(inputFilePath, 'r') as f:
    urls = f.readlines()

with ThreadPoolExecutor(max_workers=3) as executor:
    for i, url in enumerate([url.strip() for url in urls]):
        executor.submit(process_url, url, i)