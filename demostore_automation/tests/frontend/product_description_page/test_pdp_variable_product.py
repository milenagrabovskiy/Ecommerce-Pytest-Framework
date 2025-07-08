import pytest
import logging as logger
from demostore_automation.src.pages.ProductDescriptionPage import ProductDescriptionPage



@pytest.mark.usefixtures("init_driver")
class TestProductDescriptionPageVariableProduct:

    @pytest.mark.efe27
    @pytest.mark.ecomfe124
    def test_verify_product_name_displayed_variable_product(self):
        """
        This test verifies that the product name (h1 header) for a variable product is displayed.
        The variable product is hardcoded in order to keep the test frontend only.

        """
        logger.info("Starting test: test_verify_product_name_displayed_variable_product")

        #find a variable product
        product_endpoint = "product/hoodie/"
        expected_name = "Hoodie"

        #go to product page
        product_page = ProductDescriptionPage(self.driver)
        product_page.go_to_product_page(product_endpoint)

        #get displayed name
        displayed_name = product_page.get_displayed_product_name()

        #assert name matches expected
        assert displayed_name == expected_name, (f"Unexpected name displayed for variable product. Expected: {expected_name}"
                                                 f"Actual: {displayed_name}")

        logger.info("Test 'test_verify_product_name_displayed_variable_product' successfully passed")