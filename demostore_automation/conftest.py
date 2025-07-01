
import pytest
import os
import logging as logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChOptions
from selenium.webdriver.firefox.options import Options as FFOptions


@pytest.fixture(scope="class")
def init_driver(request):

    supported_browsers = ['chrome', 
                          'ch', 
                          'headlesschrome', 
                          'remote_chrome', 
                          'firefox', 
                          'ff', 
                          'headlessfirefox', 
                          'remote_firefox']

    browser = os.environ.get('BROWSER', None)
    if not browser:
        raise Exception("The environment variable 'BROWSER' must be set.")

    browser = browser.lower()

    if browser not in supported_browsers:
        raise Exception(f"Provided browser '{browser}' is not one of the supported."
                        f"Supported are: {supported_browsers}")

    if browser in ('chrome', 'ch'):
        driver = webdriver.Chrome()
    elif browser in ('firefox', 'ff'):
        driver = webdriver.Firefox()
    elif browser in ('headlesschrome'):
        logger.info("Opening Chrome headless")
        chrome_options = ChOptions()
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)

    elif browser == 'remote_chrome':
        logger.info("Starting remote Chrome")
        chrome_remote_url = os.environ.get("REMOTE_WEBDRIVER")
        if not chrome_remote_url:
            raise Exception(f"If 'browser=remote_chrome' then 'REMOTE_WEBDRIVER' variable must be set.")
        chrome_options = ChOptions()
        chrome_options.add_argument('--ignore-ssl-errors=yes')
        chrome_options.add_argument('--ignore-certificate-errors')

        driver = webdriver.Remote(
            command_executor=chrome_remote_url,
            options=chrome_options
        )

    elif browser == 'remote_firefox':
        capabilities = {
            'browserName': 'firefox',
            'marionette': True,
            'acceptInsecureCerts': True
        }
        driver = webdriver.Remote(command_executor=remote_url, desired_capabilities=capabilities)
    elif browser == 'headlessfirefox':
        ff_options = FFOptions()
        ff_options.add_argument("--disable-gpu")
        ff_options.add_argument("--no-sandbox")
        ff_options.add_argument("--headless")
        driver = webdriver.Firefox(options=ff_options)

    logger.debug("############### BROWSER INFORMATION #####################")
    for k, v in driver.capabilities.items():
        logger.debug(f"{k}: {v}")
    logger.debug("#########################################################")

    request.cls.driver = driver

    yield

    driver.quit()
