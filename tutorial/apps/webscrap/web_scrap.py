from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
import json
from collections import OrderedDict

# Setting up Selenium Webdriver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)

driver.get("https://altamontefl-energovpub.tylerhost.net/Apps/SelfService#/search")
# Wait until the search keyword input is visible
wait.until(EC.visibility_of_element_located((By.NAME, "SearchKeyword")))
input_element = driver.find_element(By.NAME, "SearchKeyword")
input_element.send_keys("")
search_button = driver.find_element(By.ID, "SearchModule")
search_button.click()

# Wait until the option element is visible and clickable
wait.until(EC.element_to_be_clickable((By.XPATH, "//option[@value='number:2' and @label='Permit']")))
option_to_select = driver.find_element(By.XPATH, "//option[@value='number:2' and @label='Permit']")
option_to_select.click()
submit_button = driver.find_element(By.ID, "button-Search")
submit_button.click()

# Wait for the page size list to be available
wait.until(EC.element_to_be_clickable((By.ID, "pageSizeList")))
page_button = driver.find_element(By.ID, "pageSizeList")
page_button.click()
option_to_select = driver.find_element(By.XPATH, "//option[@value='100' and @label='100']")
option_to_select.click()

# Wait for sufficient time for the page to load
time.sleep(5)

# Fetch and parse the HTML content
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

divs = soup.find_all('div', class_='form-inline')

records = []

for i in range(0, len(divs), 10):  # Adjust this range if the number of divs per record changes
    record_data = {}
    for j in range(10):
        if i + j >= len(divs):
            break  # Prevents going out of range
        current_div = divs[i + j]
        label = current_div.find('label')
        if label:
            if label.has_attr('aria-label'):
                label_text = label['aria-label']
            else:
                label_text = label.get_text(strip=True)

            if label_text == 'Applied Date':
                # Extracting Applied Date
                span_text = current_div.find('span').get_text(
                    strip=True
                    ) if current_div.find('span') else ''
            elif label_text == 'Address':
                # Extracting address
                tyler_highlight = current_div.find('tyler-highlight')
                span_text = tyler_highlight.find('span').get_text(
                    strip=True
                    ) if tyler_highlight and tyler_highlight.find(
                    'span'
                    ) else ''
            else:
                # Extracting other fields
                span_text = current_div.find('span').get_text(
                    strip=True
                    ) if current_div.find('span') else ''
            record_data[label_text] = span_text

    # Creating an ordered record
    record = OrderedDict([
        ("Permit Number", record_data.get('Permit Number', '')),
        ("Applied Date", record_data.get('Applied Date', '')),
        ("Type", record_data.get('Type', '')),
        ("Issued Date", record_data.get('Issued Date', '')),
        ("Project Name", record_data.get('Project Name', '')),
        ("Expiration Date", record_data.get('Expiration Date', '')),
        ("Status", record_data.get('Status', '')),
        ("Finalized Date", record_data.get('Finalized Date', '')),
        ("Main Parcel", record_data.get('Main Parcel', '')),
        ("Address", record_data.get('Address', ''))
    ])

    records.append(record)

final_json = {
    "Result": {
        "EntityResults": records
    }
}

# Convert to JSON string
json_output = json.dumps(final_json, indent=4)
print(json_output)

# Close the browser
driver.quit()