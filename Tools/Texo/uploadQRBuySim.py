import os
import time
import cv2
import json
from datetime import datetime
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


wait_time = 2
sleep_time = 1

def decodeQR(image_path):
    detector = cv2.QRCodeDetector()

    image = cv2.imread(image_path)

    data, bbox = detector.detectAndDecode(image)

    if bbox is not None:
        return data
    else:
        print("QR Code not detected")
        return None


def write_log(file_path, phone_number, img_full_path):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = {
        "timestamp": timestamp,
        "message": f"Finished add number {phone_number} - {img_full_path}"
    }
    with open(file_path, 'a') as log_file:
        json.dump(log_entry, log_file)
        log_file.write('\n')

def log_message(phone_number, img_full_path):
    write_log('./QRBuysim/log_file_uploadQRBuySim.json', phone_number, img_full_path)

def error_message(phone_number, img_full_path):
    write_log('./QRBuysim/error_file_uploadQRBuySim.json', phone_number, img_full_path)

def uploadQR(driver, image_file_path, phone_number):
		#Step 5
		#sdt
		phone_number = phone_number.replace(" ", "")
		input5 = WebDriverWait(driver, wait_time).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, 'input#code'))
		)
		input5.send_keys(phone_number)
		time.sleep(sleep_time)

		#active
		selectBox5 = WebDriverWait(driver, wait_time).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, '.select-wrapper'))
		)
		selectBox5.click()
		time.sleep(1)
  
		option = driver.find_element(By.CSS_SELECTOR, '.select-dropdown.dropdown-content li:nth-child(2)')
		option.click()
		time.sleep(sleep_time)

		#date
		input52 = WebDriverWait(driver, wait_time).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="exp_date"]'))
		)
		input52.click()
		input52.clear()
		input52.send_keys('01012030' + Keys.TAB + '0000')
		driver.execute_script("arguments[0].removeAttribute('readonly');", input52)
		driver.execute_script("arguments[0].value = '2030-01-01T00:00';", input52)
		driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", input52)
  
		time.sleep(sleep_time)

		#upload
		input53 = WebDriverWait(driver, 30).until(
			EC.presence_of_element_located((By.XPATH, '//*[@id="img"]'))
		)
  
		full_file_path = os.path.abspath(image_file_path)
		print(full_file_path)
		input53.send_keys(full_file_path)
  
		#submit
		button5 = WebDriverWait(driver, wait_time).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))
		)	
		button5.click()
		print(f"Finished add number {phone_number}")
		log_message(phone_number, full_file_path)
		time.sleep(3)
		driver.quit()


def loginHandler(parent_image_file_path, parent_phone_number, index):
	driver = webdriver.Chrome()
	try:
     
		options = webdriver.ChromeOptions()
		options.add_argument('--ignore-ssl-errors=yes')
		options.add_argument('--ignore-certificate-errors')

		posx = ((index % 3) * 350 + 10) if (index % 3) != 0 else ((index % 3) * 350)
		driver = webdriver.Chrome(options=options)
		driver.set_window_size(350, 768)
		driver.set_window_position(posx, 0)
		driver.get("https://dealeros.it-development.dev/admincp/login")

		#Step 1
		input1 = WebDriverWait(driver, wait_time).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, 'input#username'))
		)
		time.sleep(sleep_time)

		input12 = WebDriverWait(driver, wait_time).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, 'input#password'))
		)
		

		checkbox1 = WebDriverWait(driver, wait_time).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, '[type=checkbox]+span:not(.lever)'))
		)
		checkbox1.click()
		time.sleep(sleep_time)
		
		button1 = WebDriverWait(driver, wait_time).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))
		)
		button1.click()
		time.sleep(sleep_time)
		
		#Step 2
		button2 = WebDriverWait(driver, wait_time).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="https://dealeros.it-development.dev/admincp/stores/buysim/navigate"]'))
		)
		button2.click()
		time.sleep(sleep_time)
		
		#Step 3
		button3 = WebDriverWait(driver, wait_time).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, '.sidenav-main .btn-sidenav-toggle'))
		)
		button3.click()
		time.sleep(sleep_time)
		
		button32 = WebDriverWait(driver, wait_time).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="https://dealeros.it-development.dev/admincp/stores/buysim/inventory"]'))
		)
		button32.click()
		time.sleep(sleep_time)
		
		#Step 4
		button4 = WebDriverWait(driver, wait_time).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="https://dealeros.it-development.dev/admincp/stores/buysim/inventory/create"]'))
		)
		button4.click()
		time.sleep(sleep_time)

		uploadQR(driver, parent_image_file_path, parent_phone_number)
  
	except Exception as e:
		print(f"An error occurred: {e}")

def worker(image_path, index_counter):
	try:
		number = decodeQR(image_path)
		print(f"Adding number {index_counter}: {number}")
		loginHandler(image_path, number, index_counter)
	except Exception as e:
		print(f"An error occurred: {e}")
		error_message(number, image_path)
		return

def read_folder(folder_path):
    threads = []
    index_counter = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                image_path = os.path.join(root, file)
                while threading.active_count() > 3:
                    pass
                t = threading.Thread(target=worker, args=(image_path,index_counter,))
                threads.append(t)
                t.start()
                index_counter += 1
    
    for t in threads:
        t.join()
        
read_folder('./Images/QRBuysim')