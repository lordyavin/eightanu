# encoding=utf8
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
import re

FILLED_STAR_STYLE = "fill: rgb(42, 42, 47);"

COLIDX_STYLE = 0
COLIDX_NAME = 1
COLIDX_GRADE = 2
COLIDX_CRAG = 3
COLIDX_NOTES = 4
COLIDX_RATING = 5

RE_ROUTE_URL = re.compile(r"\/crags\/sportclimbing\/(?P<country>\S+)\/(?P<crag>\S+)\/sectors\/(?P<sector>\S+)\/routes\/(?P<route>\S+)")


class Ascent8a:
    """ The ascent data to export. """
    
    MAX_RATING = 5

    def __init__(self, date, style, route, grade, sector, crag, country, notes, rating):
        """
        @param date: American date
        @param style: The ascent style
        @param route: The route name
        @param grade: The route grade
        @param sector: The sector name
        @param crag: The crag name
        @param country: The country name
        @param notes: Ascent notes
        @param rating: The 5 stars based rating
        """
        self.date = date
        self.style = style
        self.route = Ascent8a._fix_route_name(route)
        self.grade = grade
        self.sector = sector
        self.crag = crag
        self.country = country
        self.notes = notes
        self.rating = rating
        
    @staticmethod
    def headers():
        return ("DATE", "STYLE", "ROUTE", "GRADE", "SECTOR", "CRAG", "COUNTRY", "NOTES", "RATING")
    
    def as_csv(self, separator=";"):        
        return separator.join((self.date,
                               self.style,
                               self.route,
                               self.grade,
                               self.sector,
                               self.crag,
                               self.country,
                               self.notes,
                               self.rating_as_stars()))

    def rating_as_stars(self):
        stars = "★" * self.rating
        stars += "☆" * (Ascent8a.MAX_RATING - self.rating)
        return stars
    
    @staticmethod
    def _fix_route_name(name):
        if "\n" in name:
            return name[:name.index("\n")]
        return name


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
    table_headers = thead.find_elements_by_tag_name("th")[1:]  # skip first empty cell
    headers = ["STYLE"] + [cell.text.strip() for cell in table_headers]
    return headers


def _determine_rating(cells):
    rating = 0
    stars = cells[COLIDX_RATING].find_elements_by_tag_name("svg")
    for star in stars:
        if star.get_attribute("style") == FILLED_STAR_STYLE:
            rating += 1
    
    return rating


def _determine_sector(cells):
    routeurl = cells[COLIDX_NAME].find_element_by_tag_name("a").get_attribute("href")
    m = re.search(RE_ROUTE_URL, routeurl)
    if m:
        return m.group("sector")
    else:
        return "unknown-sector"

    
def _determine_country(cells):
    routeurl = cells[COLIDX_NAME].find_element_by_tag_name("a").get_attribute("href")
    m = re.search(RE_ROUTE_URL, routeurl)
    if m:
        return m.group("country")
    else:
        return "unknown-country"


def _determine_style(cells):
    return cells[COLIDX_STYLE].find_element_by_tag_name("svg").get_attribute("title")


def _get_routename(cells):
    return cells[COLIDX_NAME].text


def _get_grade(cells):
    return cells[COLIDX_GRADE].text


def _get_notes(cells):
    return cells[COLIDX_NOTES].text


def _get_crag(cells):
    return cells[COLIDX_CRAG].text


def _read_ascents(table, headers):
    assert isinstance(table, WebElement)
    assert isinstance(headers, (list, tuple))
    
    ascents = []    
    groups = table.find_elements_by_tag_name("tbody")
    for group in groups:
        date = group.find_element_by_tag_name("th").text
        rows = group.find_elements_by_tag_name("tr")
        for row in rows:
            cells = row.find_elements_by_tag_name("td")  # skip first empty cell
            if len(cells) == len(headers):                
                ascent = Ascent8a(date=date,
                                  style=_determine_style(cells),
                                  route=_get_routename(cells),
                                  grade=_get_grade(cells),
                                  sector=_determine_sector(cells),
                                  crag=_get_crag(cells),
                                  country=_determine_country(cells),
                                  notes=_get_notes(cells),
                                  rating=_determine_rating(cells))              
                ascents.append(ascent)
    
    return ascents


def _print_logbook(ascents):
    assert isinstance(ascents, (list, tuple))
    
    print(";".join(Ascent8a.headers()))
    for ascent in ascents:
        print(ascent.as_csv())


def export(browser, username, verbose=0):
    assert browser in SUPPORTED_BROWSER
    assert isinstance(username, str)
    assert isinstance(verbose, int)    
    
    username = username.replace(" ", "-").lower()
    url = "https://www.8a.nu/user/{username}/sportclimbing".format(username=username)
    
    if verbose:
        print("Exporting ascents from %s at" % username)
        print("%s ..." % url)
       
    driver = webdriver.get(browser, verbose)
    try:
        driver.get(url)
        _select_alltime_ascents(driver)
        _sort_by_date(driver)
        
        table = driver.find_element_by_class_name("user-ascents")       
        headers = _read_table_headers(table)
        ascents = _read_ascents(table, headers)       
        _print_logbook(ascents)
    finally:
        driver.close()
