from demostore_automation.src.configs.MainConfigs import MainConfigs
from demostore_automation.src.pages.locators.ProductDescriptionPageLocators import ProductDescriptionPageLocators
from demostore_automation.src.selenium_extended.SeleniumExtended import SeleniumExtended


class ProductDescriptionPage(ProductDescriptionPageLocators):

    def __init__(self, driver):
        self.driver = driver
        self.sl = SeleniumExtended(driver)


    def go_to_product_page(self, product_endpoint):

        base_url = MainConfigs.get_base_url()
        product_url = f"{base_url}/{product_endpoint}"
        self.sl.go_to_url(product_url)


    def get_displayed_product_name(self):
        return self.sl.wait_and_get_text(self.PRODUCT_TITLE)