'''
eightanu.export -- The 8a.nu logbook export

@author:     lordyavin
@copyright:  2020 lordyavin. All rights reserved.
@license:    MIT
@contact:    github@klesatschke.net
@deffield    updated: Updated
'''
from selenium.webdriver.remote.webelement import WebElement

from eightanu import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from eightanu.webdriver import SUPPORTED_BROWSER

def _select_alltime_ascents(driver):
    assert isinstance(driver, WebDriver)
    
    filters = driver.find_element_by_class_name("ascent-filters")    
    assert isinstance(filters, WebElement)
    
    all_options = filters.find_elements_by_tag_name("option")
    for option in all_options:
        if option.text == "All Time":
            option.click()

def _sort_by_date(driver):
    assert isinstance(driver, WebDriver)
    
    order = driver.find_element_by_class_name("ascent-filters__order")
    all_options = order.find_elements_by_tag_name("option")
    for option in all_options:
        if option.text == "Date":
            option.click()


def _read_table_headers(table):
    assert isinstance(table, WebElement)
    
    thead = table.find_element_by_tag_name("thead")
    table_headers = thead.find_elements_by_tag_name("th")[1:] # skip first empty cell
    headers = ["DATE", "STYLE"] + [cell.text.strip() for cell in table_headers]
    return headers


def _read_ascents(table, headers):
    assert isinstance(table, WebElement)
    assert isinstance(headers, (list, tuple))
    
    ascents = []
    name_idx = headers.index("NAME")
    groups = table.find_elements_by_tag_name("tbody")
    for group in groups:
        date = group.find_element_by_tag_name("th").text
        rows = group.find_elements_by_tag_name("tr")
        for row in rows:
            cells = row.find_elements_by_tag_name("td") # skip first empty cell
            if len(cells) == len(headers)-1:
                style = cells[0].find_element_by_tag_name("svg").get_attribute("title")
                ascent = [date, style] + [cell.text.strip() for cell in cells[1:]]
                name = ascent[name_idx]
                if "\n" in name:
                    ascent[name_idx] = name[:name.index("\n")]
                ascents.append(ascent)
    
    return ascents


def _print_logbook(headers, ascents):
    assert isinstance(headers, (list, tuple))
    assert isinstance(ascents, (list, tuple))
    
    print(";".join(headers))
    for ascent in ascents:
        print(";".join(ascent))

def export(browser, username, verbose=0):
    assert browser in SUPPORTED_BROWSER
    assert isinstance(username, str)
    assert isinstance(verbose, int)    
    
    username = username.replace(" ", "-").lower()
    url = "https://www.8a.nu/user/{username}/sportclimbing".format(username=username)    
       
    driver = webdriver.get(browser, verbose)
    try:
        driver.get(url)
        _select_alltime_ascents(driver)
        _sort_by_date(driver)
        
        table = driver.find_element_by_class_name("user-ascents")       
        headers = _read_table_headers(table)
        ascents = _read_ascents(table, headers)       
        _print_logbook(headers, ascents)
    finally:
        driver.close()
