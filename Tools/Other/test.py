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
import zipfile
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

PROXY_HOST = '103.14.155.117'  # rotating proxy or host
PROXY_PORT = 37590  # port
PROXY_USER = 'irjy5s1b'  # username
PROXY_PASS = 'iRjY5s1b'  # password

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

def get_chromedriver(use_proxy=False, user_agent=None):
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    
    service = Service(os.path.join(path, 'chromedriver'))
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def process_url(url, index):
    
    options = Options()

    # set the proxy address
    proxy_server_ip = f'http://{PROXY_HOST}:{PROXY_PORT}'
    # proxy_server_ip = f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}'
    options.add_argument(f"--proxy-server={proxy_server_ip}")

    driver = webdriver.Chrome(options)
    # driver = webdriver.Chrome(
    #     seleniumwire_options={
    #         'proxy': {
    #         'http': f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}',
    #         },
    #     }
    # )  # or whichever browser you prefer

    # Get screen size
    screen_width = driver.execute_script("return window.screen.availWidth")
    screen_height = driver.execute_script("return window.screen.availHeight")

    # Set window size and position
    quarter_screen_width = screen_width // 4
    driver.set_window_size(quarter_screen_width, 700)
    driver.set_window_position(quarter_screen_width * (index % 4), 0)

    driver = get_chromedriver(use_proxy=True)
    # driver.get('https://www.google.com/search?q=my+ip+address')
    driver.get('https://httpbin.org/ip')
    
    # driver.get(url)
    
    time.sleep(1000)

    
    
    driver.quit()



with open('./Input/Dick/Dick20240812-2.txt', 'r') as f:
    urls = f.readlines()

with ThreadPoolExecutor(max_workers=1) as executor:
    for i, url in enumerate([url.strip() for url in urls]):
        executor.submit(process_url, url, i)