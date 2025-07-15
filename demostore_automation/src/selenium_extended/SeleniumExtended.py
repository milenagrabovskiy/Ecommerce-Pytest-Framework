
import time

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

class SeleniumExtended:
    """Helper class extending Selenium WebDriver with convenience methods and smart waits.

    This class wraps common Selenium interactions with built-in explicit waits
    to improve test stability and reduce code duplication.

    Attributes:
        driver (WebDriver): Selenium WebDriver instance.
        default_timeout (int): Default wait time for explicit waits in seconds.
    """

    def __init__(self, driver):
        """Initializes the SeleniumExtended class.

        Args:
            driver (WebDriver): Selenium WebDriver instance.
        """
        self.driver = driver
        self.default_timeout = 5

    def go_to_url(self, url):
        """Navigate to a specific URL.

        Args:
            url (str): The URL to navigate to.
        """
        self.driver.get(url)

    def wait_and_input_text(self, locator, text, timeout=None):
        """Wait for visibility of element, then input text.

        Args:
            locator (tuple): Locator for the element.
            text (str): Text to input.
            timeout (int, optional): Max wait time in seconds.
        """
        timeout = timeout if timeout else self.default_timeout

        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        ).send_keys(text)

    def wait_and_click(self, locator, timeout=None):
        """Wait for element to be clickable and click it.

        Args:
            locator (tuple): Locator for the element.
            timeout (int, optional): Max wait time in seconds.
        """
        timeout = timeout if timeout else self.default_timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            ).click()
        except StaleElementReferenceException:
            time.sleep(2)
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator),
                message=f"Element with locator {locator}, is not clickable."
            ).click()

    def wait_until_element_contains_text(self, locator, text, timeout=None):
        """Wait until the element contains specific text.

        Args:
            locator (tuple): Locator for the element.
            text (str): Text to wait for.
            timeout (int, optional): Max wait time in seconds.
        """

        timeout = timeout if timeout else self.default_timeout

        WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(locator, text),
            message=f'Element with locator = {locator}, does not contain text: "{text}", after waiting {timeout} seconds.'
        )

    def wait_until_element_is_visible(self, locator_or_element, timeout=None):
        """Wait until element is visible.

        Args:
            locator_or_element (tuple or WebElement): Locator tuple or WebElement instance.
            timeout (int, optional): Max wait time in seconds.

        Returns:
            WebElement: The visible element.

        Raises:
            TypeError: If the input is not a tuple or WebElement.
        """
        timeout = timeout if timeout else self.default_timeout

        if isinstance(locator_or_element, tuple):
            elem = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator_or_element),
                message=f"Element with locator {locator_or_element} not found after timeout of {timeout}"
            )
        else:
            import selenium.webdriver.remote.webelement
            if isinstance(locator_or_element, selenium.webdriver.remote.webelement.WebElement):
                elem = WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of(locator_or_element),
                    message=f"Element {locator_or_element} not found after timeout of {timeout}"
                )
            else:
                raise TypeError(f"The locator to check visibility must be a 'tuple' or a 'WebElement'. It was {type(locator_or_element)}")

        return elem

    def wait_and_get_elements(self, locator, timeout=None, err=None):
        """Wait for all elements matching locator to be visible.

        Args:
            locator (tuple): Locator for the elements.
            timeout (int, optional): Max wait time in seconds.
            err (str, optional): Custom error message.

        Returns:
            list: List of WebElement instances.

        Raises:
            TimeoutException: If elements are not found in time.
        """
        timeout = timeout if timeout else self.default_timeout
        err = err if err else f"Unable to find elements located by '{locator}'," \
                              f"after timeout of {timeout}"
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_all_elements_located(locator),
            )
        except TimeoutException:
            raise TimeoutException(err)

        return elements

    def wait_and_select_dropdown(self, locator, to_select, select_by='visible_text'):
        """Wait for dropdown and select an option.

        Args:
            locator (tuple): Locator for the <select> element.
            to_select (str or int): Option to select.
            select_by (str): 'visible_text', 'index', or 'value'.

        Raises:
            Exception: If select_by value is invalid.
        """

        select_element = self.wait_until_element_is_visible(locator)
        select = Select(select_element)
        if select_by.lower() == 'visible_text':
            select.select_by_visible_text(to_select)
        elif select_by.lower() == 'index':
            select.select_by_index(to_select)
        elif select_by.lower() == 'value':
            select.select_by_value(to_select)
        else:
            raise Exception(f"Invalid option for 'to_select' parameter. Valid values are 'visible_text', 'index', or value 'value'.")

    def wait_and_get_text(self, locator, timeout=None):
        """Wait for element to be visible and get its text.

        Args:
            locator (tuple): Locator for the element.
            timeout (int, optional): Max wait time in seconds.

        Returns:
            str: Text content of the element.
        """
        timeout = timeout if timeout else self.default_timeout
        elm = self.wait_until_element_is_visible(locator, timeout)
        element_text = elm.text

        return element_text


