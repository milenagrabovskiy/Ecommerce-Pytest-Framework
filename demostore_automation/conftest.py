
import pytest
import os
import logging as logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChOptions
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.firefox.service import Service as FFService
import tempfile



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
        logger.info("Starting remote Chrome")
        chrome_remote_url = os.environ.get("REMOTE_WEBDRIVER")
        if not chrome_remote_url:
            raise Exception(f"If 'browser=remote_chrome' then 'REMOTE_WEBDRIVER' variable must be set.")

        chrome_options = ChOptions()
        chrome_options.add_argument('--ignore-ssl-errors=yes')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Remote(command_executor=chrome_remote_url, options=chrome_options)

    elif browser == 'remote_firefox':
        remote_url = os.environ.get("REMOTE_WEBDRIVER")
        if not remote_url:
            raise Exception("REMOTE_WEBDRIVER must be set for remote_firefox")

        ff_options = FFOptions()
        ff_options.accept_insecure_certs = True
        driver = webdriver.Remote(
        command_executor=remote_url,
        options=ff_options
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



import pytest
import logging as logger
from demostore_automation.src.api_helpers.OrdersAPIHelper import OrdersAPIHelper
from demostore_automation.src.api_helpers.ProductsAPIHelper import ProductsAPIHelper
from demostore_automation.src.dao.products_dao import ProductsDAO
from demostore_automation.src.generic_helpers.generic_orders_helper import GenericOrdersHelper

@pytest.fixture(scope="module")
def my_orders_smoke_setup():
    """Setup fixture for creating and cleaning up test orders.

    Fetches a random product from the database and prepares API helpers.
    Tracks created orders for teardown after tests complete.

    Yields:
        dict: {
                "product_id" (int): Random product ID from DB,
                "product_price" (float): Product price,
                "orders_api_helper" (OrdersAPIHelper): Helper for order API calls,
                "order_ids" (list[int]): Tracks created order IDs for teardown
            }
        """
    products_dao = ProductsDAO()
    product_api_helper = ProductsAPIHelper()
    random_product = products_dao.get_random_product_from_db(qty=1)[0]
    product_id = random_product['ID']
    logger.info(f"Fetched random product from DB: {random_product}")
    product_details = product_api_helper.call_get_product_by_id(product_id)
    product_price = product_details['price']
    info = {
            "product_id": random_product['ID'],
            "product_price": product_price,
            "orders_api_helper": OrdersAPIHelper(),
            "generic_orders_helper": GenericOrdersHelper(),
            "order_ids": []
        }
    yield info

    for ord_id in info["order_ids"]:
        info["orders_api_helper"].call_delete_order(ord_id)
        logger.info(f"Successfully deleted order id: {ord_id}")
    logger.info(f"Successfully deleted {len(info['order_ids'])} orders")