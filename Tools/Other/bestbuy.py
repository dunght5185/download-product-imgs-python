import os
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import os
import shutil
from urllib.parse import urlparse

def download_image(url, save_as):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(url, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
            print(f"Downloaded image to {save_as}")
    else:
        print(f"Failed to download image from {url}")

image_url = 'https://pisces.bbystatic.com/image2/BestBuy_US/exc/videometadata/thumbnail/de9794edba89fad3e876083ad8cd5ab9.jpg'
save_as = 'image.jpg'

download_image(image_url, save_as)

# def download_image(url, save_dir):
#     r = requests.get(url, stream=True)
#     if r.status_code == 200:
#         # Parse the URL to get the image name
#         a = urlparse(url)
#         img_name = os.path.basename(a.path)

#         # Join the save directory path with the image name
#         img_path = os.path.join(save_dir, img_name)

#         with open(img_path, 'wb') as f:
#             r.raw.decode_content = True
#             shutil.copyfileobj(r.raw, f)
#             print(f"Downloaded image to {img_path}")