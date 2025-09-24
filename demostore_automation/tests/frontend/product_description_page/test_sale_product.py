"""Module for testing sale product functionality in DemoStore.
Includes verification of sale badges on product pages and in the cart.
"""
import pytest
from demostore_automation.src.pages.CartPage import CartPage
from demostore_automation.src.pages.HomePage import HomePage
from demostore_automation.src.pages.ProductDescriptionPage import ProductDescriptionPage
from demostore_automation.src.pages.Header import Header

pytestmark = [pytest.mark.sale_product]

@pytest.mark.usefixtures("init_driver", "setup")
class TestOnSaleProduct:
    """Tests for sale products in DemoStore.

    Attributes:
        home_page (HomePage): Home page interactions.
        pdp (ProductDescriptionPage): Product detail page interactions.
        header (Header): Site header interactions.
        cart_page (CartPage): Shopping cart interactions.
    """
    @pytest.fixture(scope='class')
    def setup(self, request):
        """Initialize page objects and navigate to the first product.

        This fixture sets up the page objects for HomePage, ProductDescriptionPage,
        Header, and CartPage, then navigates to the home page and clicks the first product.

        Args:
            self (TestOnSaleProduct): Instance of the test class.
            request (FixtureRequest): Provides access to pytest fixture request.
        """
        request.cls.home_page = HomePage(self.driver)
        request.cls.pdp = ProductDescriptionPage(self.driver)
        request.cls.header = Header(self.driver)
        request.cls.cart_page = CartPage(self.driver)
        request.cls.home_page.go_to_home_page()
        request.cls.home_page.click_on_first_product()

    @pytest.mark.efe44
    def test_verify_sale_sign_displayed(self):
        """Verify sale sign and original price on product page.
        Checks that the sale badge is visible and the original price is crossed out.
        """
        # verify sale sign visible
        self.pdp.verify_on_sale_sign_displayed()

        # verify orig price crossed out
        self.pdp.verify_orig_price_crossed_out()

    @pytest.mark.efe45
    def test_verify_sale_in_cart(self):
        """Verify sale badge appears correctly in the cart.

        Adds the first product to the cart and checks that the discounted price is displayed.
        """
        # click add to cart
        self.home_page.click_first_add_to_cart_button()
        self.header.click_on_cart_on_right_header()

        # verify it says 'save orig-sale price'
        self.cart_page.verify_sale_badge_displayed()