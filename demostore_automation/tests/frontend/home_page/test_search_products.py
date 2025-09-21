import time
import logging as logger
import pytest
from demostore_automation.src.pages.HomePage import HomePage
from demostore_automation.src.pages.Header import Header
from demostore_automation.src.pages.ProductDescriptionPage import ProductDescriptionPage
from demostore_automation.src.utilities.genericUtilities import generate_random_string

pytestmark = [pytest.mark.feregression, pytest.mark.fesmoke, pytest.mark.home_page]

@pytest.mark.parametrize(
    ("product_type", "product_name"),
    [
        pytest.param('simple', 'Album', marks=pytest.mark.efe, id='search for simple product'),
        pytest.param('variable', 'Hoodie', marks=pytest.mark.efe, id='search for variable product'),
        pytest.param('invalid', generate_random_string(), marks=pytest.mark.efe, id='search for nonexisting product')
    ]
)

@pytest.mark.usefixtures("init_driver")
class TestHomePageSmoke:

    @pytest.fixture(scope='class')
    def setup(self, request):
        request.cls.home_page = HomePage(self.driver)
        request.cls.header = Header(self.driver)
        request.cls.pdp = ProductDescriptionPage(self.driver)
        self.home_page.go_to_home_page()

    @pytest.mark.efe123
    def test_search_for_simple_product(self, setup, product_type, product_name):
        if product_type == 'simple':
            product_name = 'Album'
            self.home_page.search_for_product_by_name(product_name)
            pdp_product = self.pdp.get_displayed_product_name()
            assert pdp_product == product_name, (f"Search for product by name loaded wrong product."
                                                 f"Expected product: {product_name}, Actual: {pdp_product}")

        elif product_type == 'variable':
            self.home_page.search_for_product_by_name(product_name)
            all_product_names = self.home_page.get_all_product_names()
            assert product_name in all_product_names, (f"Product not present on home page after searching by name."
                                                       f"All products: {all_product_names}")


        elif product_type == 'invalid':
            self.home_page.go_to_home_page()
            self.home_page.search_for_product_by_name(product_name)
            # assert product_name in all_products, "Product not present on home page after searching by name"

        logger.info(f"Successfully ran test for {product_type}, {product_name}")