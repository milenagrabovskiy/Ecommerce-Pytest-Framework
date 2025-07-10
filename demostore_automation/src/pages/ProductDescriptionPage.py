from demostore_automation.src.configs.MainConfigs import MainConfigs
from demostore_automation.src.pages.locators.ProductDescriptionPageLocators import ProductDescriptionPageLocators
from demostore_automation.src.selenium_extended.SeleniumExtended import SeleniumExtended
import logging as logger
import re

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

    def get_url_of_displayed_image(self):
        """
           Retrieves the main product image URL from the product description page. Removes suffix using re

           Returns:
               str: The cleaned image URL without WooCommerce sizing suffix.
           """
        image_elm = self.sl.wait_until_element_is_visible(self.PRODUCT_MAIN_IMAGE)
        image_url = image_elm.get_attribute('src')

        cleaned_url = re.sub(r'-\d+x\d+(?=\.jpg)', '', image_url)

        return cleaned_url


    def get_urls_of_displayed_alternate_images(self):
        """
           Retrieves the main product image URL from the product description page. Removes suffix using re

           Returns:
               list: The cleaned image URLs without WooCommerce sizing suffix.
           """
        image_elements = self.sl.wait_and_get_elements(self.PRODUCT_ALTERNATE_IMAGES)
        original_image_urls = [image.get_attribute('src') for image in image_elements]

        cleaned_urls = []

        for image_url in original_image_urls:
            # using re to replace woocommerce thumbnail size with an empty string
            cleaned_url = re.sub(r'-\d+x\d+(?=\.jpg)', '', image_url)
            cleaned_urls.append(cleaned_url)

        return cleaned_urls


