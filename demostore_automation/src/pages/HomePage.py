from selenium.webdriver import Keys
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
        return [product.text for product in products] #returns a list of strings (product names)

    def verify_no_products_found_msg(self):
        error = 'No products were found matching your selection.'
        self.sl.wait_until_element_contains_text(self.NO_PRODUCTS_MSG_LOCATOR, error)

    def get_sorting_dropdown_menu(self):
        return self.sl.wait_until_element_is_visible(self.SORTING_MENU)

    def get_product_images(self):
        return self.sl.wait_and_get_elements(self.PRODUCT_IMAGES)

    def get_product_prices(self):
        return self.sl.wait_and_get_elements(self.PRICES)

    def get_product_names(self):
        return self.sl.wait_and_get_elements(self.PRODUCT_NAMES) # returns the name elements