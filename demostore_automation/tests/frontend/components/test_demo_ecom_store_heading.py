"""Tests for the Demo eCom Store header component.

This module verifies that the site header behaves consistently across different pages.
It ensures that clicking the store header always redirects the user to the homepage
and that the header text is displayed correctly.
"""
import pytest
from demostore_automation.src.pages.CartPage import CartPage
from demostore_automation.src.pages.HomePage import HomePage
from demostore_automation.src.pages.Header import Header
from demostore_automation.src.pages.MyAccountSignedOutPage import MyAccountSignedOutPage

pytestmark = [pytest.mark.feregression, pytest.mark.fesmoke, pytest.mark.header, pytest.mark.components]

@pytest.mark.usefixtures("init_driver")
class TestHeader:
    """Smoke and regression tests for the Demo eCom Store header.

    This test class focuses on verifying the behavior of the
    store header link across multiple pages, ensuring that
    users are always redirected to the homepage and that
    the correct header text is displayed.
    """

    @pytest.fixture(scope="class")
    def setup_pages(self, request):
        """Initialize page objects once per test class."""
        request.cls.header = Header(self.driver)
        request.cls.home_page = HomePage(self.driver)
        request.cls.cart_page = CartPage(self.driver)
        request.cls.my_acc_so = MyAccountSignedOutPage(self.driver)

    @pytest.mark.parametrize(
        "page",
        [
            pytest.param('my_account', marks=pytest.mark.efe53),
            pytest.param('cart', marks=pytest.mark.efe54)
        ]
    )

    def test_demo_ecom_heading_redirects_to_homepage(self, setup_pages, page):
        """Verify that clicking the store header redirects to the homepage.

        Args:
            setup_pages: Fixture providing initialized page objects.
            page (str): Starting page where the test begins.
                        Can be either "my_account" or "cart".
        """
        # go to starting page
        if page == 'my_account':
            self.my_acc_so.go_to_my_account()

        elif page == 'cart':
            self.cart_page.go_to_cart_page()

        self.header.click_on_store_header()

        products = self.home_page.get_all_product_elements()
        assert products, f"Products not displayed after clicking site header. Expected to redirect to home page"

    @pytest.mark.efe55
    def test_verify_store_header_text(self, setup_pages):
        """Verify that the store header text is displayed correctly.

        Args:
            setup_pages: Fixture providing initialized page objects.

        Asserts:
            The store header text equals the expected header string.
        """
        self.home_page.go_to_home_page()
        expected_header = 'Demo eCom Store'
        store_header = self.header.get_store_header_text()
        assert store_header == expected_header, (f"Error. Wrong store header. Actual: {store_header},"
                                                 f"Expected: {expected_header}")