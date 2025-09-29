from selenium.webdriver import Keys
from selenium.webdriver.support.ui import Select
from demostore_automation.src.selenium_extended.SeleniumExtended import SeleniumExtended
from demostore_automation.src.configs.MainConfigs import MainConfigs
from demostore_automation.src.pages.locators.HomePageLocators import HomePageLocators

class HomePage(HomePageLocators):

    def __init__(self, driver):
        self.driver = driver
        self.sl = SeleniumExtended(driver)

    def go_to_home_page(self):
        base_url = MainConfigs.get_base_url()
        self.driver.get(base_url)

    def click_first_add_to_cart_button(self):
        self.sl.wait_and_click(self.ADD_TO_CART_BTN)

    def click_first_product(self):
        self.sl.wait_and_click(self.FIRST_PRODUCT)

    def get_all_product_elements(self):
        error_msg = "Can not get product elements from home page."

        # products_elm = self.sl.wait_and_get_elements(self.PRODUCT, err=error_msg)
        # return products_elm

        return self.sl.wait_and_get_elements(self.PRODUCT, err=error_msg)

    def get_displayed_heading(self):
        return self.sl.wait_and_get_text(self.PAGE_HEADING)

    def search_for_product_by_name(self, product_name):
        search_field = self.sl.wait_until_element_is_visible(self.SEARCH_BAR_FIELD)
        search_field.clear()
        search_field.send_keys(product_name + Keys.ENTER)

    def get_all_product_names(self):
        products = self.sl.wait_and_get_elements(self.PRODUCT_NAMES)
        return [product.text for product in products]

    def verify_no_products_found_msg(self):
        error = 'No products were found matching your selection.'
        self.sl.wait_until_element_contains_text(self.NO_PRODUCTS_MSG_LOCATOR, error)

    def verify_sorting_menu_displayed(self):
        dropdown_menu = self.sl.wait_until_element_is_visible(self.SORTING_MENU)
        select = Select(dropdown_menu) #using select class because element is a select element (with select tag).
        options = select.options
        assert len(options) > 1

    def verify_product_images_displayed(self):
        images = self.sl.wait_and_get_elements(self.PRODUCT_IMAGES)
        for image in images:
            assert image.is_displayed(), "Error. Product images are not displayed in UI"

    def verify_product_prices_displayed(self):
        prices = self.sl.wait_and_get_elements(self.PRICES)
        for price in prices:
            assert price.is_displayed(), "Error. Product prices are not displayed in UI"

    def verify_product_names_displayed(self):
        names = self.sl.wait_and_get_elements(self.PRODUCT_NAMES)
        for name in names:
            assert name.is_displayed(), "Error. Product prices are not displayed in UI."
