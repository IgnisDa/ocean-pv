import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture()
def selenium_options():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--incognito")
    return chrome_options


@pytest.fixture()
def selenium_driver(selenium_options):

    drivers = []

    def _make_selenium_driver(use=True):
        if use is True:
            driver = webdriver.Chrome(
                executable_path='tests/integration/webdrivers/chromedriver',
                options=selenium_options)
            drivers.append(driver)
            return driver
        else:
            driver = webdriver.Chrome(
                executable_path='tests/integration/webdrivers/chromedriver',
                options=None)
            drivers.append(driver)
            return driver

    yield _make_selenium_driver

    for driver in drivers:
        driver.close()
