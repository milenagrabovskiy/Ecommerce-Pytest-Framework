from demostore_automation.src.configs.MainConfigs import MainConfigs
from demostore_automation.src.pages.locators.ProductDescriptionPageLocators import ProductDescriptionPageLocators
from demostore_automation.src.selenium_extended.SeleniumExtended import SeleniumExtended
import logging as logger
import re

class ProductDescriptionPage(ProductDescriptionPageLocators):
    """Page object model for the product description page.

    Inherits:
        ProductDescriptionPageLocators: Provides locators for elements on the product page.

    This class provides methods to interact with and extract data from the WooCommerce
    product detail view, including the product name, main image, and alternate images.

    Attributes:
        driver (WebDriver): Selenium WebDriver instance.
        sl (SeleniumExtended): Extended Selenium utility wrapper for smart waits and interactions.
    """
    def __init__(self, driver):
        """Initializes the ProductDescriptionPage with a WebDriver.

        Args:
            driver (WebDriver): Selenium WebDriver instance.
        """
        self.driver = driver
        self.sl = SeleniumExtended(driver)

    def go_to_product_page(self, product_endpoint):
        """Navigates to a specific product page.

        Args:
            product_endpoint (str): URL endpoint of the product (e.g., 'product/my-shirt').
        """
        base_url = MainConfigs.get_base_url()
        product_url = f"{base_url}/{product_endpoint}"
        self.sl.go_to_url(product_url)

    def get_displayed_product_name(self):
        """Gets the product name displayed on the page.

        Returns:
            str: Product name as shown in the H1 title.
        """
        return self.sl.wait_and_get_text(self.PRODUCT_TITLE)

    def get_url_of_displayed_image(self):
        """Retrieves the main product image URL without WooCommerce sizing suffix.

        Returns:
            str: The cleaned main product image URL (e.g., without '-300x300' suffix).
        """
        image_elm = self.sl.wait_until_element_is_visible(self.PRODUCT_MAIN_IMAGE)
        image_url = image_elm.get_attribute('src')

        cleaned_url = re.sub(r'-\d+x\d+(?=\.jpg)', '', image_url)

        return cleaned_url


    def get_urls_of_displayed_alternate_images(self):
        """Retrieves all alternate product image URLs, cleaned of WooCommerce sizing suffixes.

        Returns:
            list[str]: A list of cleaned image URLs.
        """
        image_elements = self.sl.wait_and_get_elements(self.PRODUCT_ALTERNATE_IMAGES)
        original_image_urls = [image.get_attribute('src') for image in image_elements]

        cleaned_urls = []

        for image_url in original_image_urls:
            # using re to replace woocommerce thumbnail size with an empty string
            cleaned_url = re.sub(r'-\d+x\d+(?=\.jpg)', '', image_url)
            cleaned_urls.append(cleaned_url)

        return cleaned_urls

    def click_on_reviews_link(self):
        self.sl.wait_and_click(self.REVIEWS_LINK)

    def click_on_stars_rating(self):
        # self.sl.wait_until_element_is_visible(self.PRODUCT_REVIEW_STARS)
        self.sl.wait_and_click(self.PRODUCT_REVIEW_STARS)

    def write_product_review(self, review_text):
        self.sl.wait_and_input_text(self.REVIEW_FIELD, review_text)

    def write_reviewer_name(self, name):
        self.sl.wait_and_input_text(self.REVIEW_NAME_FIELD, name)

    def write_reviewer_email(self, email):
        self.sl.wait_and_input_text(self.REVIEW_EMAIL_FIELD, email)

    def click_submit_and_verify_success(self):
        self.sl.wait_and_click(self.SUBMIT_BTN)
        self.sl.wait_until_element_contains_text(self.SUCCESS_MSG, 'Your review is awaiting approval')