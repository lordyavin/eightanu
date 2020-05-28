'''
Created on 28.05.2020

@author: klesatschke
'''
from selenium.webdriver.remote.webelement import WebElement

from eightanu import webdriver


def export(browser, username):
    url = "https://www.8a.nu/user/{username}/sportclimbing".format(username=username)    
       
    driver = webdriver.get(browser)
    driver.get(url)
    filters = driver.find_element_by_class_name("ascent-filters")
    assert isinstance(filters, WebElement)
    all_options = filters.find_elements_by_tag_name("option")
    for option in all_options:
        if option.get_attribute("value") == "0":
            option.click()
    
    table = driver.find_element_by_class_name("user-ascents")
    assert isinstance(table, WebElement)
    
    table_headers = table.find_elements_by_tag_name("th")
    print(", ".join([cell.text for cell in table_headers]))
    
    rows = table.find_elements_by_tag_name("tr")
    for row in rows:
        cells = row.find_element_by_class_name("td")
        print(", ".join([cell.text for cell in cells]))
    
    driver.close()
