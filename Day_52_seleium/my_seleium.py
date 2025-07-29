from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:

    driver.get("https://secure-retreat-92358.herokuapp.com/")

    first_name = driver.find_element(By.NAME, "fName")
    first_name.send_keys("jjj")

    last_name = driver.find_element(By.CSS_SELECTOR, ".form-control.middle")
    last_name.send_keys("hehehehe")

    email = driver.find_element(By.NAME, "email")
    email.send_keys("asdf@asdf.com")
    time.sleep(3)
    button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-lg.btn-primary.btn-block")
    button.click()
    time.sleep(5)
