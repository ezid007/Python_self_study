# 이름, 이메일 주소 자동입력 및 클릭
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rich import print
import time
import os

os.system('cls')

url = 'https://secure-retreat-92358.herokuapp.com/'

chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(chrome_option)

driver.get(url)

first_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'fName')))
first_name.send_keys("Angela")

last_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'lName')))
last_name.send_keys('Yu')

email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email')))
email.send_keys("angela@email.com")

submit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn')))
submit.click()

time.sleep(5)
