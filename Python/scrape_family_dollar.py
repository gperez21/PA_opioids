# Scrape family dollar locations for PA from locator website
# Gabriel Perez-Putnam 2/21/19

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import time


def sleep_time(x):
    """Sleep for X seconds times a number between 0 and 1"""
    random_time = random.random() *2* x
    time.sleep(random_time)

def find_cities(driver):
    """Pull the urls of all the cities listed"""
    driver.get(DT_url)
    # links = driver.find_elements_by_xpath("//div[@class='content_area']//a[]")
    links = driver.find_elements_by_class_name("itemlist")
    # driver.find_element_by_partial_link_text('https://www.dollartree.com/locations/pa/')
    urls = []
    for link in links:
        urls.append(link.find_element_by_tag_name('a').get_attribute("href"))
    return urls

def get_city_stores(driver,city):
    driver.get(city)
    stores = driver.find_elements_by_css_selector(".itemlist.forcitypage")
    store_list = []
    for store in stores:
        att_list = []
        store_address = store.get_attribute('innerText').split("\n")
        for p in store_address:
            att_list.append(p)
        store_list.append(att_list)
    print(store_list)
    return store_list

def clean_row_for_export(variables):
    """Prepares a row of data for export"""
    row = (',').join(variables) + '\n'
    return row

def export_to_file(file_name, stores_info):
    """Export the beer information to a file"""
    with open(file_name, 'w+', encoding='utf-8') as f:
        header = ['Store_Number', 'Address', 'City', 'State_Zip']
        export_header = clean_row_for_export(header)
        f.write(export_header)
        for city in stores_info:
            for store in city:
                row = clean_row_for_export(store)
                f.write(row)

def iterate_states(driver):
    """Go through the list and return the indivisible info"""
    cities = find_cities(driver)
    all_stores = []
    for city in cities:
        print(city)
        sleep_time(5)
        stores = get_city_stores(driver,city)
        all_stores.append(stores)
    return all_stores

def main():
    """controller"""
    # create a new Chrome session
    driver = webdriver.Chrome(executable_path='C:/Users/perez_g/Desktop/Web Scrapping/env/Scripts/chromedriver.exe')
    # driver.maximize_window()
    driver.implicitly_wait(30)

    # URL of initial search
    global DT_url
    DT_url = "https://locations.familydollar.com/pa/"
    stores_info = iterate_states(driver)
    export_to_file('family_dollar_locations.txt', stores_info)

main()
