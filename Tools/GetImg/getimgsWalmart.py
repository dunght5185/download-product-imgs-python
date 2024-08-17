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

num = 1
dateTime = 'Walmart20240704'

def download_image(url, save_dir, file_format='webp'):
    r = requests.get(url, stream=True)
    fileType = url.split('.')[-1]

    if r.status_code == 200:
        if fileType == 'webp':
            # Parse the URL to get the image name
            a = urlparse(url)
            img_name = os.path.basename(a.path)

            # Open the image with PIL
            img = Image.open(BytesIO(r.content))

            # Change the file extension to the desired format
            # img_name = os.path.splitext(img_name)[0] + '.' + file_format.lower()

            # Join the save directory path with the image name
            safe_dir_path = re.sub('[^A-Za-z0-9]+', '_', save_dir)

            img_path = os.path.join(safe_dir_path, img_name)
            # img_path = os.path.join(save_dir, img_name)

            # Save the image in the desired format
            img.save(img_path, file_format.upper())
            print(f"Done______________{img_path}")
        else:
            # Parse the URL to get the image name
            print(url, save_dir)
            a = urlparse(url)
            img_name = os.path.basename(a.path)

            # Join the save directory path with the image name
            img_path = os.path.join(save_dir, img_name)

            with open(img_path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            print(f"Done______________{img_path}")
    else:
        print(f"Error downloading image: {r.status_code}")

userAgent = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 11_15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6312.207 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6275.197 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6304.198 Safari/537.36']
def process_url(url, index):
    options = Options()
    
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--headless=new') # for Chrome >= 109
    # Avoiding detection
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option("useAutomationExtension", False) 
    

    s = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=s, options=options)
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": userAgent[index % 4]}) 
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 

    # driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome(options=options)
    # Get screen size
    screen_width = driver.execute_script("return window.screen.availWidth")
    screen_height = driver.execute_script("return window.screen.availHeight")

    # Set window size and position
    quarter_screen_width = screen_width // 4
    driver.set_window_size(300, 700)
    driver.set_window_position(300 * (index % 4), 0)

    driver.get(url)


    # You'll need to adjust the following lines based on the website structure
    try:
        product_name = driver.find_element(By.CSS_SELECTOR, 'h1').text.replace('/', '-')
    except Exception as e:
        print(f"Error getting product name: {e}")


    try:
        # Wait for at least one image to be present
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.container[data-testid="vertical-carousel-container"] .tc.overflow-hidden.br3 img')))

        # Get image elements
        image_elements = driver.find_elements(By.CSS_SELECTOR, '.container[data-testid="vertical-carousel-container"] .tc.overflow-hidden.br3 img')
        
    except Exception as e:
        print(f"Error getting product name: {e}")




    # Create a directory for the product images
    save_dir = os.path.join(os.getcwd(), f'Images/Walmart/{dateTime}/{num}', product_name)
    os.makedirs(save_dir, exist_ok=True)

    # Download each image
    for i, image_element in enumerate(image_elements):
        print('Downloading image: ', i)
        image_url = image_element.get_attribute("src")
        imgURL = image_url.split('?')[0]
        print(imgURL, save_dir)
        download_image(imgURL, save_dir)
        # print('Downloaded image: ', image_url)

    print(f"Finished processing {product_name}")
    print('............................. \n\n')
    driver.quit()

    time.sleep(5)  # delay for 5 seconds

with open(f'./Input/{dateTime}/Walmart.txt', 'r') as f:
    urls = f.readlines()

with ThreadPoolExecutor(max_workers=4) as executor:
    for i, url in enumerate([url.strip() for url in urls]):
        executor.submit(process_url, url, i)
        if i != 0 and (i+1) % 4 == 0:
            time.sleep(90)

