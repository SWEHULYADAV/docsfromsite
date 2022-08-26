from re import search
import selenium
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")


pgcount = 0
err_count = 0
while True:
    if err_count < 100: 
        try:
            pgcount=pgcount+1
            url = "https://indiankanoon.org/doc/"+str(pgcount)
            driver.get(url)
            search = driver.find_element(By.XPATH, "//input[@value='Get this document in PDF']")  
            search.click()
            print("DOCUMENT NO: "+ str(pgcount) +" DOWNLOADED")
        except:      #exceptional condition
            err_count += 1
