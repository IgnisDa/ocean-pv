import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


@pytest.mark.browser
def test_random(selenium_driver, live_server):
    driver = selenium_driver()  # type: webdriver.Chrome()
    driver.get(live_server.url)
    assert 'IgnisDa' in driver.current_url


if __name__ == '__main__':
    pytest.main()
