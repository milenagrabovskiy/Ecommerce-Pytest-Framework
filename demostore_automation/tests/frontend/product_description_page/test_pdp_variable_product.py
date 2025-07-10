import pytest
import logging as logger
from demostore_automation.src.pages.ProductDescriptionPage import ProductDescriptionPage
from demostore_automation.src.api_helpers.ProductsAPIHelper import ProductsAPIHelper


@pytest.mark.usefixtures("init_driver")
class TestProductDescriptionPageVariableProduct:

    @pytest.fixture(scope="class")
    def setup(self, request):
        """
          Class-level fixture that prepares test data and navigates to the product page.

          - Sets expected product name and ID.
          - Fetches product image URLs from the WooCommerce API.
          - Initializes the ProductDescriptionPage and navigates to the product detail page.
        """
        # hardcoding variable product
        product_endpoint = "product/hoodie/"
        request.cls.expected_name = "Hoodie"
        request.cls.product_id = 20

        # api get call for product info
        product_api_helper = ProductsAPIHelper()
        product_info = product_api_helper.call_get_product_by_id(request.cls.product_id)
        images = product_info['images']
        request.cls.api_image_urls = [image.get('src') for image in images]

        # go to pdp
        request.cls.product_page = ProductDescriptionPage(self.driver)
        request.cls.product_page.go_to_product_page(product_endpoint)

    @pytest.mark.efe27
    @pytest.mark.ecomfe124
    def test_verify_product_name_displayed_variable_product(self, setup):
        """
        This test verifies that the product name (h1 header) for a variable product is displayed.
        The variable product is hardcoded in order to keep the test frontend only.

        """
        logger.info("Starting test: 'test_verify_product_name_displayed_variable_product'")

        #get displayed name
        displayed_name = self.product_page.get_displayed_product_name()

        #assert name matches expected
        assert displayed_name == self.expected_name, (f"Unexpected name displayed for variable product. Expected: {self.expected_name}"
                                                 f"Actual: {displayed_name}")

        logger.info("Test 'test_verify_product_name_displayed_variable_product' successfully passed")

    @pytest.mark.efe28
    @pytest.mark.ecom125
    def test_verify_main_image_variable_prod(self, setup):
        """
            Verifies the main product image on the frontend matches one returned by the API.
        """
        logger.info("Starting test: 'test_verify_main_image_variable_prod'")

        displayed_image_url = self.product_page.get_url_of_displayed_image()
        logger.info(f"Displayed image url: {displayed_image_url}")

        #verify url is valid
        assert displayed_image_url.startswith('http') and displayed_image_url.endswith('.jpg'), \
            "Invalid image url. Must start with 'http' and end with '.jpg'"

        assert displayed_image_url in self.api_image_urls, "Displayed image url not found in api"



    @pytest.mark.efe29
    @pytest.mark.ecom126
    def test_verify_alternate_images_variable_prod(self, setup):
        """
           Verifies that all alternate product images displayed on the frontend
           match the image URLs returned by the WooCommerce API.

           This comparison ignores the order of images but requires an exact URL match.
        """
        logger.info("Starting test: 'test_verify_alternate_images_variable_prod'")

        displayed_image_urls = self.product_page.get_urls_of_displayed_alternate_images()

        assert sorted(displayed_image_urls) == sorted(self.api_image_urls), "Displayed image urls do not match api image urls."


