
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

    def get_all_product_elements(self):
        error_msg = "Can not get product elements from home page."

        # products_elm = self.sl.wait_and_get_elements(self.PRODUCT, err=error_msg)
        # return products_elm

        return self.sl.wait_and_get_elements(self.PRODUCT, err=error_msg)

    def get_displayed_heading(self):
        return self.sl.wait_and_get_text(self.PAGE_HEADING)