# encoding: utf-8
import os
import sys
from zipfile import ZipFile

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import urllib3
from urllib3.response import HTTPResponse

FIREFOX_DRIVER_URL = "https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-win64.zip"
CHROME_DRIVER_URL = "https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_win32.zip"

FIREFOX = "Firefox"
CHROME = "Chrome"

SUPPORTED_BROWSER = (
    FIREFOX,
    CHROME,
)

DOWNLOAD = {
    FIREFOX: FIREFOX_DRIVER_URL,
    CHROME: CHROME_DRIVER_URL
}

DRIVER = {
    FIREFOX: webdriver.Firefox,
    CHROME: webdriver.Chrome,
}


def download(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    assert isinstance(response, HTTPResponse)
    zipfilename = os.path.basename(url)
    
    with open(zipfilename, "wb") as zipfile:
        zipfile.write(response.data)
        
    with ZipFile(zipfilename) as zipfile:
        zipfile.extractall(".")

    os.remove(zipfilename)


def get(browser):
    assert browser in SUPPORTED_BROWSER
    try:     
        driver = DRIVER[browser]()
    except WebDriverException:
        download(DOWNLOAD[browser])
        driver = webdriver.Firefox()
    return driver
