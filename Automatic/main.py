from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, InvalidArgumentException
from bs4 import BeautifulSoup
import time
import json
import os
import requests
from urllib.parse import urljoin, urlparse

# Function to initialize Selenium WebDriver
def initialize_driver():
    options = webdriver.ChromeOptions()
    # Add options as needed: headless, etc.
    driver = webdriver.Chrome(service=Service(executable_path=r"C:\Users\12\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"), options=options)
    return driver

# Function to navigate to a URL and return page source
def navigate_to_url(driver, url):
    try:
        print(f"Navigating to URL: {url}")
        driver.get(url)
        time.sleep(2)  # Adjust as needed
    except InvalidArgumentException as e:
        print(f"Error navigating to URL: {url} - {e}")
    except Exception as e:
        print(f"Error navigating to URL: {url} - {e}")

# Function to find all links on a page
def find_links(driver, tag_name):
    return driver.find_elements(By.TAG_NAME, tag_name)

# Function to click a button based on its ID
def click_button(driver, button_id):
    try:
        button = driver.find_element(By.ID, button_id)
        button.click()
        return True
    except NoSuchElementException:
        return False

# Function to download PDFs
def download_pdf(driver, pdf_url, download_folder):
    driver.get(pdf_url)
    time.sleep(3)  # Allow time for the PDF to download
    # Implement PDF download logic here
    # For example, you can use the requests library to download the PDF
    response = requests.get(pdf_url, stream=True)
    if response.status_code == 200:
        with open(os.path.join(download_folder, "document.pdf"), "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

# Main scraping function
def scrape_indian_kanoon(driver):
    navigate_to_url(driver, "https://indiankanoon.org/browse/union-act/")

    pdf_folder = os.path.abspath("pdfs_folder")
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)

    while True:
        all_links = find_links(driver, "a")
        for link in all_links:
            url = link.get_attribute("href")
            if url and "union-act" in url:
                navigate_to_url(driver, url)

                # Click on "Entire Year" link if available
                try:
                    entire_year_link = driver.find_element(By.LINK_TEXT, "Entire Year")
                    if entire_year_link:
                        entire_year_link.click()
                        time.sleep(2)  # Allow time for the page to load

                        # Parse HTML content using BeautifulSoup
                        soup = BeautifulSoup(driver.page_source, 'html.parser')

                        # Find <div> element with class "results_middle"
                        results_middle_div = soup.find('div', {'class':'results_middle'})

                        # Extract all links within the <div> element
                        links = [a['href'] for a in results_middle_div.find_all('a', href=True)]

                        # Filter out invalid URLs
                        valid_links = []
                        for link in links:
                            parsed_url = urlparse(link)
                            if parsed_url.netloc and parsed_url.scheme:
                                valid_links.append(link)
                            else:
                                valid_links.append(urljoin("https://indiankanoon.org", link))

                        # Iterate over the links
                        for link in valid_links:
                            navigate_to_url(driver, link)

                            # Find <button> element with ID "pdfdoc"
                            soup = BeautifulSoup(driver.page_source, 'html.parser')
                            pdf_button = soup.find('button', {'id': 'pdfdoc'})

                            # Click on the button to initiate PDF download
                            if pdf_button:
                                pdf_button_element = driver.find_element(By.ID, "pdfdoc")
                                pdf_button_element.click()
                                time.sleep(2)  # Allow time for the PDF download dialog to appear

                                # Download the PDF file using requests
                                pdf_url = driver.current_url
                                response = requests.get(pdf_url, stream=True)
                                if response.status_code == 200:
                                    with open(os.path.join(pdf_folder, "document.pdf"), "wb") as f:
                                        for chunk in response.iter_content(1024):
                                            f.write(chunk)

                                # Collect metadata and store in JSON
                                metadata = {
                                    "title": driver.title,
                                    "url": pdf_url,
                                    # Add more fields as needed
                                }
                                with open("metadata.json", "a") as f:
                                    json.dump(metadata, f)
                                    f.write("\n")

                                # Go back to the document listing page
                                driver.back()

                            # Check if there are any remaining links on the page
                            remaining_links = driver.find_elements(By.TAG_NAME, "a")
                            if remaining_links:
                                print("Remaining links found on the page. Re-visiting...")
                                for remaining_link in remaining_links:
                                    navigate_to_url(driver, remaining_link.get_attribute("href"))
                                    # Repeat the PDF download process for each remaining link
                                    #...

                except NoSuchElementException:
                    print(f"No 'Entire Year' link found for URL: {url}")

        # Check if there are any remaining links on the main page
        remaining_links = driver.find_elements(By.TAG_NAME, "a")
        if not remaining_links:
            break

    driver.quit()

# Initialize WebDriver
driver = initialize_driver()

# Execute the scraping function
scrape_indian_kanoon(driver)