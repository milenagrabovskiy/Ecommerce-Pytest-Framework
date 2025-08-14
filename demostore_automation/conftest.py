
import pytest
import os
import logging as logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChOptions
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.firefox.service import Service as FFService



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
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)

    elif browser == 'remote_chrome':

        remote_url = os.environ.get("REMOTE_WEBDRIVER")
        if not remote_url:
            raise Exception("If 'browser=remote_chrome', 'REMOTE_WEBDRIVER' must be set.")
        chrome_options = ChOptions()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")  # required for CI
        capabilities = chrome_options.to_capabilities()
        capabilities['acceptInsecureCerts'] = True

        driver = webdriver.Remote(
        command_executor=remote_url,
        desired_capabilities=capabilities
        )
    elif browser == 'remote_firefox':
        remote_url = os.environ.get("REMOTE_WEBDRIVER")
        if not remote_url:
            raise Exception("If 'browser=remote_firefox', 'REMOTE_WEBDRIVER' must be set.")

        ff_options = FFOptions()
        ff_options.add_argument("--disable-gpu")
        ff_options.add_argument("--no-sandbox")
        # ff_options.add_argument("--headless")  # optional for CI

        capabilities = ff_options.to_capabilities()
        capabilities['acceptInsecureCerts'] = True

        driver = webdriver.Remote(
            command_executor=remote_url,
            desired_capabilities=capabilities
        )
    elif browser == 'headlessfirefox':
        ff_options = FFOptions()
        ff_options.add_argument("--disable-gpu")
        ff_options.add_argument("--no-sandbox")
        ff_options.add_argument("--headless")
        service = FFService(executable_path="/usr/local/bin/geckodriver")
        driver = webdriver.Firefox(service=service, options=ff_options)

    logger.debug("############### BROWSER INFORMATION #####################")
    for k, v in driver.capabilities.items():
        logger.debug(f"{k}: {v}")
    logger.debug("#########################################################")

    request.cls.driver = driver

    yield

    driver.quit()