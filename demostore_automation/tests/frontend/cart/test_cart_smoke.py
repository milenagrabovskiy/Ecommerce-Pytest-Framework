"""Frontend tests for verifying the empty cart page functionality.

This module contains smoke and regression tests that validate the behavior
of the cart page when no products are added. It ensures that the correct
empty cart message is displayed and that the "New In Store" section
is visible to users even when the cart is empty.
"""
import pytest

from demostore_automation.conftest import init_driver
from demostore_automation.src.pages.CartPage import CartPage
from demostore_automation.src.pages.HomePage import HomePage

pytestmark = [pytest.mark.feregression, pytest.mark.fesmoke, pytest.mark.smoke, pytest.mark.cart]

@pytest.fixture(scope='class')
def setup_cart_page(request):
    """Fixture to initialize the CartPage object once per test class."""
    request.cls.cart_page = CartPage(request.cls.driver)
    request.cls.cart_page.go_to_cart_page()

@pytest.mark.usefixtures("init_driver")
class TestCartSmoke:
    """Test suite for validating the behavior of an empty cart page."""
    @pytest.mark.efe59
    def test_verify_empty_cart_by_default(self, setup_cart_page):
        """Verify that the cart is empty by default when no products are added.

        This test checks that the correct empty cart message is displayed
        when a user visits the cart page without adding any products.

        Expected Result:
            The page should display the message: "Your cart is currently empty!".
        """
        expected_message = 'Your cart is currently empty!'
        message = self.cart_page.verify_empty_cart()
        assert message == expected_message, (f"ERROR. Empty cart message does not match expected."
                                             f"Actual: {message}, Expected: {expected_message}")

    @pytest.mark.efe60
    def test_verify_new_products_displayed(self, setup_cart_page):
        """Verify that 'New In Store' products are displayed when the cart is empty.

        This test ensures that even when the user's cart is empty,
        the "New In Store" section appears with the appropriate heading.

        Expected Result:
            The heading should read "New in store", and the section should be visible.
        """
        expected_heading = "New in store"
        heading = self.cart_page.get_new_in_store_heading()
        assert heading == expected_heading, f"ERROR. Wrong heading. Expected: {expected_heading}, Actual: {heading}"

    @pytest.mark.efe61
    def test_verify_cart_heading(self, setup_cart_page):
        """Verify that the cart page heading is displayed correctly.

        This test checks that the cart page displays the correct heading text
        to confirm that the user is on the Cart page.
        """
        expected_heading = 'Cart'
        heading = self.cart_page.get_cart_header()
        assert heading == expected_heading, (f"ERROR. Wrong heading on cart page."
                                             f"Expected: {expected_heading}, Actual: {heading}")
