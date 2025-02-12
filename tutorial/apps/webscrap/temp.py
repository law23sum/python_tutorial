from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
import time
import concurrent.futures


def setup_driver():
    options = Options()
    options.headless = True  # Change to False if you need to debug
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 30)
    return driver, wait


def navigate_to_search_page(driver, wait, search_keyword):
    try:
        driver.get("https://altamontefl-energovpub.tylerhost.net/Apps"
                   "/SelfService#/search")

        wait.until(EC.invisibility_of_element_located((By.ID, "overlay")))
        wait.until(EC.element_to_be_clickable((By.ID, "SearchModule")))
        time.sleep(5)
        search_button = driver.find_element(By.ID, "SearchModule")
        ActionChains(driver).move_to_element(search_button).click(
                search_button).perform()

        wait.until(EC.element_to_be_clickable((By.XPATH,
                                               "//option[@value='number:2' "
                                               "and @label='Permit']")))
        option_to_select = driver.find_element(By.XPATH, "//option["
                                                         "@value='number:2' "
                                                         "and "
                                                         "@label='Permit']")
        option_to_select.click()

        wait.until(EC.visibility_of_element_located((
                By.NAME, "SearchKeyword")))
        search_textbox = driver.find_element(By.NAME, "SearchKeyword")
        search_textbox.clear()
        search_textbox.send_keys(search_keyword)
        search_textbox.send_keys(Keys.ENTER)
        time.sleep(5)  # Wait for sufficient time for the page to load

        submit_button = driver.find_element(By.ID, "button-Search")
        submit_button.click()

        wait.until(EC.element_to_be_clickable((By.ID, "pageSizeList")))
        page_button = driver.find_element(By.ID, "pageSizeList")
        page_button.click()

        wait.until(EC.element_to_be_clickable((By.ID, "pageSizeList")))
        page_button = driver.find_element(By.ID, "pageSizeList")
        page_button.click()
        option_to_select = driver.find_element(By.XPATH, "//option[@value='100' and @label='100']")
        option_to_select.click()
        time.sleep(5)  # Wait for sufficient time for the page to load

    except Exception as e:
        print(f"Error in navigate_to_search_page: {e}")
        driver.quit()


def process_page(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    divs = soup.find_all('div', class_='form-inline')
    page_records = []

    for i in range(0, len(divs), 10):
        record_data = {}
        for j in range(10):
            if i + j >= len(divs):
                break
            current_div = divs[i + j]
            label = current_div.find('label')
            if label:
                if label.has_attr('aria-label'):
                    label_text = label['aria-label']
                else:
                    label_text = label.get_text(strip=True)

                span_text = current_div.find('span').get_text(strip=True) if \
                    current_div.find('span') else ''
                record_data[label_text] = span_text

        record = OrderedDict([
                (
                        "Permit Number",
                        record_data.get('Permit Number', '')),
                ("Applied Date", record_data.get('Applied Date', '')),
                ("Type", record_data.get('Type', '')),
                ("Issued Date", record_data.get('Issued Date', '')),
                ("Project Name", record_data.get('Project Name', '')),
                ("Expiration Date",
                 record_data.get('Expiration Date', '')),
                ("Status", record_data.get('Status', '')),
                ("Finalized Date",
                 record_data.get('Finalized Date', '')),
                ("Main Parcel", record_data.get('Main Parcel', '')),
                ("Address", record_data.get('Address', ''))
        ])
        page_records.append(record)

    return page_records

def select_descending(driver):
    sort_button = driver.find_element(By.ID, "SortAscending")
    sort_button.click()
    descend_option = driver.find_element(
            By.XPATH, "//*[@id='SortAscending']/option[2]"
    )
    descend_option.is_selected()
    descend_option.is_enabled()
    descend_option.click()
    pass

def click_next_page(driver, wait):
    try:
        next_page_button = wait.until(EC.element_to_be_clickable((By.ID,
                                                                  "link-NextPage")))
        next_page_button.click()
    except Exception as e:
        print(f"Error in click_next_page: {e}")
        return False
    return True


def scrape_keyword(keyword):
    driver, wait = setup_driver()
    try:
        navigate_to_search_page(driver, wait, keyword)
        current_page = 0
        file_name = f"altamonte_json/scraped_data_{keyword}.json"
        with open(file_name, 'w') as file:
            file.write('{"Result": {"EntityResults": [')

        while current_page < 100:
            page_source = driver.page_source
            page_records = process_page(page_source)

            json_output = json.dumps(page_records, indent=4)
            with open(file_name, 'a') as file:
                if current_page > 0:
                    file.write(', ')
                file.write(json_output[1:-1])

            print(f"Keyword {keyword} - Page {current_page + 1}: Process"
                  f"ed {len(page_records)} records")

            if not click_next_page(driver, wait):
                print(f"Keyword {keyword} - End of pages or error navigating.")
                break
            current_page += 1
            time.sleep(5)

        with open(file_name, 'a') as file:
            file.write(']}}')

    except Exception as e:
        print(f"Error in scrape_keyword for {keyword}: {e}")
    finally:
        driver.quit()

def scrape_keyword(keyword):
    driver, wait = setup_driver()
    try:
        navigate_to_search_page(driver, wait, keyword)
        current_page = 0
        max_page = 0
        count = 0
        file_name = f"altamonte_json/scraped_data_{keyword}.json"
        with open(file_name, 'w') as file:
            file.write('{"Result": {"EntityResults": [')

        while max_page < 2:
            while current_page < 100:
                page_source = driver.page_source
                page_records = process_page(page_source)
                count += len(page_records)
                json_output = json.dumps(page_records, indent=4)

                with open(file_name, 'a') as file:
                    if current_page > 0:
                        file.write(', ')
                    file.write(json_output[1:-1])

                print(f"Keyword {keyword} - Page {current_page + 1}: Processed {len(page_records)} records, Total so far: {count}")

                if not click_next_page(driver, wait):
                    print(f"Keyword {keyword} - End of pages or error navigating.")
                    break

                current_page += 1
                time.sleep(5)

            try:
                total_records_element = driver.find_element(By.CLASS_NAME, 'ng-binding')
                total_records_text = total_records_element.text
                total_records = int(total_records_text.replace("Found ", "").replace(" results", "").replace(",", ""))
                print(f"Total records for keyword {keyword}: {total_records}")
            except NoSuchElementException as e:
                print(f"Could not retrieve total records for keyword {keyword}: {e}")

            if total_records >= 1000:
                select_descending(driver)

            max_page += 1
            time.sleep(5)

        with open(file_name, 'a') as file:
            file.write(']}}')

    except Exception as e:
        print(f"Error in scrape_keyword for {keyword}: {e}")
    finally:
        driver.quit()

def main():
    search_keywords = ['1*-0*', '1*-00*', '2*-0*', '2*-*0', '3*-0*', '4*-0*',
                       '5*-0*', '6*-0*', '7*-0*', '8*-0*', '91*-0*', '92*-0*',
                       '93*-0*', '94*-0*', '95*-0*', '96*-0*', '97*-0*',
                       '98*-0*', '99*-0*']

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        executor.map(scrape_keyword, search_keywords)


if __name__ == "__main__":
    main()