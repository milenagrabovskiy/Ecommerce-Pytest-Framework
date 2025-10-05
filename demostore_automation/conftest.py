
import pytest
import os
import pytest_html
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChOptions
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.firefox.service import Service as FFService
import tempfile
import logging as logger
from demostore_automation.src.api_helpers.OrdersAPIHelper import OrdersAPIHelper
from demostore_automation.src.api_helpers.ProductsAPIHelper import ProductsAPIHelper
from demostore_automation.src.dao.products_dao import ProductsDAO
from demostore_automation.src.generic_helpers.generic_orders_helper import GenericOrdersHelper
from demostore_automation.src.pages.MyAccountSignedOutPage import MyAccountSignedOutPage
from demostore_automation.src.pages.MyAccountSignedInPage import MyAccountSignedInPage
from demostore_automation.src.utilities.genericUtilities import generate_random_email_and_password


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

@pytest.fixture(scope='class')
def create_registered_user(request):
    driver = request.cls.driver
    my_acct_page = MyAccountSignedOutPage(driver)
    my_acct_page.go_to_my_account()

    email_password = generate_random_email_and_password()
    email = email_password['email']
    password = email_password['password']

    my_acct_page.input_register_email(email)
    my_acct_page.input_register_password(password)
    my_acct_page.click_register_button()

    my_acct_si = MyAccountSignedInPage(driver)
    my_acct_si.verify_user_is_signed_in()

    return {'email': email, 'password': password}


# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#         outcome = yield
#         report = outcome.get_result()
#         extras = getattr(report, "extras", [])
#         if report.when == "call":
#             # always add url to report
#             extras.append(pytest_html.extras.url("http://www.example.com/"))
#             xfail = hasattr(report, "wasxfail")
#             if (report.skipped and xfail) or (report.failed and not xfail):
#                 is_frontend = True if 'init_driver' in item.fixturenames else False
#                 if is_frontend:
#                     results_dir = os.environ.get('RESULTS_DIR')
#                     screenshot_path = os.path.join(results_dir, item.name + '.png')
#                     driver_fixture = item.funcargs['request']
#                     driver = driver_fixture.cls.driver.save_screenshot(screenshot_path)
#                     if not results_dir:
#                         raise Exception("'RESULTS_DIR env variable must be set")
#                 # only add additional html on failure
#                 extras.append(pytest_html.extras.image(screenshot_path))
#             report.extras = extras
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        is_frontend = 'init_driver' in item.fixturenames
        if is_frontend:
            results_dir = os.environ.get("RESULTS_DIR", os.path.join(tempfile.gettempdir(), "screenshots"))
            os.makedirs(results_dir, exist_ok=True)

            screenshot_path = os.path.join(results_dir, f"{item.name}.png")
            driver = item.instance.driver
            driver.save_screenshot(screenshot_path)

            if hasattr(report, "extras"):
                import pytest_html
                report.extras.append(pytest_html.extras.image(screenshot_path))