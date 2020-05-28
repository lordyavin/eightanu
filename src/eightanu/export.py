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


def export(browser, username, verbose=0):
    username = username.replace(" ", "-").lower()
    url = "https://www.8a.nu/user/{username}/sportclimbing".format(username=username)    
       
    driver = webdriver.get(browser, verbose)
    try:
        driver.get(url)
        filters = driver.find_element_by_class_name("ascent-filters")
        assert isinstance(filters, WebElement)
        all_options = filters.find_elements_by_tag_name("option")
        for option in all_options:
            if option.text == "All Time":
                option.click()
                
        order = driver.find_element_by_class_name("ascent-filters__order")
        all_options = order.find_elements_by_tag_name("option")
        for option in all_options:
            if option.text == "Date":
                option.click()
        
        table = driver.find_element_by_class_name("user-ascents")
        assert isinstance(table, WebElement)
        
        thead = table.find_element_by_tag_name("thead")
        table_headers = thead.find_elements_by_tag_name("th")
        table_headers = ["DATE"] + [cell.text.strip() for cell in table_headers]
        print(", ".join(table_headers))
        
        groups = table.find_elements_by_tag_name("tbody")
        for group in groups:
            date = group.find_element_by_tag_name("th").text
            rows = group.find_elements_by_tag_name("tr")
            for row in rows:
                cells = row.find_elements_by_tag_name("td")
                if cells:
                    cells = [date] + [cell.text.strip() for cell in cells]
                    print(", ".join(cells))
    finally:
        driver.close()
