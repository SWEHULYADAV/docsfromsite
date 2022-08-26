#importing some requirements
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox") 
driver = webdriver.Chrome(service=Service(executable_path=os.environ.get("CHROMEDRIVER_PATH")), options=chrome_options)

driver.page_source
#creating variable
pgcount = 0
err_count = 0

#code

while True:
    if err_count < 5: 
        try:
            pgcount=pgcount+1
            err_count = 0
            url = "https://indiankanoon.org/doc/"+str(pgcount)  #link of the site which we scrapped 
            driver.get(url)
            print(driver.page_source)
            #variable with xpath 
            search = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, "//input[@value='Get this document in PDF']")))
            print(driver.page_source)
            search.click() #automating code to click and download Docs
            print("DOCUMENT NO: "+ str(pgcount) +" DOWNLOADED")
        except Exception as e:      #exceptional condition
            print(e.args,e.message)
            err_count += 1
