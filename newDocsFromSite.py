#importing some requirements
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pymongo

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Provide the correct path to Chrome binary
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

# Initialize Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Set timeout duration for page load
driver.set_page_load_timeout(120)  # 120 seconds

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["indiankanoon"]  # Choose or create your MongoDB database
collection = db["documents"]  # Choose or create your collection

# Main script
pgcount = 0
err_count = 0

while True:
    if err_count < 5: 
        try:
            pgcount += 1
            err_count = 0
            url = "https://indiankanoon.org/doc/" + str(pgcount)  # Link of the site which we are scraping 
            driver.get(url)
            
            # Extract information from web page
            page_content = driver.page_source
            soup = BeautifulSoup(page_content, 'html.parser')
            
            # Example: Extract title
            title = soup.find("title").text
            
            # Example: Extract content
            content = soup.find("div", {"class": "content"}).text
            
            # Store extracted information in MongoDB
            document = {
                "title": title,
                "content": content
            }
            collection.insert_one(document)
            
            print("Document No:", pgcount, "stored in MongoDB")

            # Variable with XPath
            search = WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.XPATH, "//input[@value='Get this document in PDF']"))
            )

            # Check if element is found
            if search:
                print(driver.page_source)
                search.click() # Automating code to click and download Docs
                print("DOCUMENT NO: " + str(pgcount) + " DOWNLOADED")
            else:
                print("Element not found. Skipping...")
                
        except Exception as e:      # Exceptional condition
            print("An error occurred:", e)
            err_count += 1
    else:
        print("Maximum error count reached. Exiting loop.")
        break

# Close the WebDriver session
driver.quit()
