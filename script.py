from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

import pandas as pd, numpy as np
import time, sys

url = "https://www.brainyquote.com/"
# absolute path need to setup
chrome_driver_path = "/home/nazmul/Documents/myProjects/scrapper/brainy-quote-sellenium/chromedriver_linux64/chromedriver"

chrome_options = Options()
chrome_options.add_argument("--headless")

webdriver = webdriver.Chrome(
    executable_path=chrome_driver_path,
    options = chrome_options
    )

# search query
search_query = "life"

if len(sys.argv) >= 2:
    search_query = sys.argv[1]

print("Search Query: {0}".format(search_query))

final_data = []

with webdriver as driver:
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    search = driver.find_element_by_id("hmSearch")
    search.send_keys(search_query + Keys.RETURN)
    
    wait.until(presence_of_element_located((By.ID, "quotesList")))
    results = driver.find_elements_by_class_name("m-brick")
    
    for quote in results:
        quoteArr = quote.text.split('\n')
        final_data.append(quoteArr)
        # print(quoteArr)
        # print()
    
    driver.close()

labels = ['Quote', 'Writer', 'Tags']
export_dataframe = pd.DataFrame.from_records(final_data, columns=labels)
export_dataframe.to_csv(search_query + "_quote.csv")

print("Complete!")