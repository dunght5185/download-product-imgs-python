from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# Initialize the driver
driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)

# Now you can use `driver`
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[-1])