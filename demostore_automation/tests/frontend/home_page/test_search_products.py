"""Tests for product search functionality on the home page.
Includes simple, variable, and non-existing product searches.
"""
import logging as logger
import pytest
from demostore_automation.src.pages.HomePage import HomePage
from demostore_automation.src.pages.Header import Header
from demostore_automation.src.pages.ProductDescriptionPage import ProductDescriptionPage
from demostore_automation.src.configs.MainConfigs import MainConfigs

pytestmark = [pytest.mark.feregression, pytest.mark.home_page]

@pytest.mark.parametrize(
    "product_type",
    [
        pytest.param('simple', marks=[pytest.mark.efe39, pytest.mark.fesmoke, pytest.mark.smoke],
                                                                  id='search for simple product'),
        pytest.param('variable', marks=pytest.mark.efe40, id='search for variable product'),
        pytest.param('invalid', marks=pytest.mark.efe41, id='search for nonexisting product')
    ]
)

@pytest.mark.usefixtures("init_driver")
class TestSearchProduct:
    """Home page search bar product search tests for simple, variable, and invalid products."""
    @pytest.fixture(scope='class')
    def setup(self, request):
        request.cls.home_page = HomePage(self.driver)
        request.cls.header = Header(self.driver)
        request.cls.pdp = ProductDescriptionPage(self.driver)
        request.cls.config = MainConfigs()
        self.home_page.go_to_home_page()

    @pytest.mark.efe123
    def test_search_up_product(self, setup, product_type):
        """Verifies product search results by product type.

        Args:
            setup: Test fixture to initialize page objects.
            product_type (str): Type of product to search ('simple', 'variable', 'invalid').

        Assertions:
            - Simple product: Navigates to PDP and matches product name.
            - Variable product: Product is listed on the home page.
            - Invalid product: Displays 'no products found' message.
        """
        product_name = self.config.get_product_name_by_type(product_type)
        self.home_page.go_to_home_page()
        self.home_page.search_for_product_by_name(product_name)

        if product_type == 'simple':
            pdp_product = self.pdp.get_displayed_product_name()
            assert pdp_product == product_name, (f"Search for product by name loaded wrong product."
                                                 f"Expected product: {product_name}, Actual: {pdp_product}")

        elif product_type == 'variable':
            all_product_names = self.home_page.get_all_product_names()
            assert product_name in all_product_names, (f"Product not present on home page after searching by name."
                                                       f"All products: {all_product_names}")
        elif product_type == 'invalid':
            self.home_page.verify_no_products_found_msg()

        logger.info(f"Successfully ran test for {product_type} product, {product_name}")