import os
import time
from selenium import webdriver

def process_url():
    driver = webdriver.Chrome()

    screen_width = driver.execute_script("return window.screen.availWidth")
    screen_height = driver.execute_script("return window.screen.availHeight")

    driver.set_window_size(screen_width, screen_height)
    driver.set_window_position(0, 0)

    # driver.get(url)
    driver.get('http://dev:BemiDevelopment2024@dev.bemi.health')
    time.sleep(100)


    driver.quit()

process_url()