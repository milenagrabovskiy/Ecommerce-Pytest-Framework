"""Tests for verifying shopping cart persistence behavior for both registered and guest users.

This module contains automated tests to ensure that:
- A registered user's cart persists after logging out and logging back in.
- A guest user's cart does not persist after the browser session ends (simulated by clearing cookies).

These tests validate proper session and data persistence behavior across user authentication states.
"""
import pytest
from demostore_automation.conftest import init_driver
from demostore_automation.src.pages.HomePage import HomePage
from demostore_automation.src.pages.CartPage import CartPage
from demostore_automation.src.pages.Header import Header
from demostore_automation.src.pages.MyAccountSignedInPage import MyAccountSignedInPage
from demostore_automation.src.pages.MyAccountSignedOutPage import MyAccountSignedOutPage

pytestmark = [pytest.mark.feregression, pytest.mark.my_account, pytest.mark.cart, pytest.mark.cart_persistence]

@pytest.fixture(scope='class')
def setup_fixture(request):
    """Initialize page objects and add an item to the cart before tests."""
    request.cls.my_acct_so = MyAccountSignedOutPage(request.cls.driver)
    request.cls.my_acct_si = MyAccountSignedInPage(request.cls.driver)
    request.cls.home_page = HomePage(request.cls.driver)
    request.cls.header = Header(request.cls.driver)
    request.cls.cart_page = CartPage(request.cls.driver)

    # go to home page and add first item to cart
    request.cls.home_page.go_to_home_page()
    request.cls.home_page.click_first_add_to_cart_button()


@pytest.mark.usefixtures("init_driver")
class TestCartPersistenceAfterLogout:
    """Test suite for verifying shopping cart persistence after logout or session end.

    This class includes tests for:
      * Registered users — ensuring that cart items persist after logging out and back in.
      * Guest users — ensuring that cart contents are cleared after the session ends.

    Each test follows the Arrange–Act–Assert structure and uses Selenium-based
    page objects to interact with the frontend.
    """
    @pytest.mark.efe58
    def test_cart_persistence_after_logout(self, create_registered_user, setup_fixture):
        """Verify that a registered user's cart persists after logging out and logging back in.

        This test ensures that when a registered user adds an item to their shopping cart,
        logs out, and then logs back in, the item remains in their cart.
        It validates that the application correctly maintains the user's cart data
        across authenticated sessions.

        Args:
            create_registered_user (dict): Fixture that creates and returns a registered
                user's credentials (email and password).

        Expected Result:
            The product added before logging out remains in the cart after logging back in.
        """
        # make registered user via conftest.py fixture
        email = create_registered_user['email']
        password = create_registered_user['password']


        # add item to cart
        first_product = 'Album'

        # logout
        self.my_acct_so.go_to_my_account()

        self.my_acct_si.click_logout()

        # login
        self.my_acct_so.input_login_username(email)
        self.my_acct_so.input_login_password(password)
        self.my_acct_so.click_login_button()

        # verify cart still contains item
        self.header.wait_until_cart_item_count(1)
        self.header.click_on_cart_on_right_header()

        products_in_cart = self.cart_page.get_all_product_names_in_cart()
        assert first_product in products_in_cart, (f"Product added before logging out not in cart."
                                                   f"Product(s) in cart: {products_in_cart}")

    @pytest.mark.efe57
    def test_guest_cart_does_not_persist_after_session_end(self, setup_fixture):
        """Verify that a guest user's cart does not persist after browser session ends.

        This test ensures that when a guest (unauthenticated) user adds an item to their cart
        and then the browser session ends (simulated by clearing cookies),
        the cart becomes empty when the user revisits the site.
        It validates that guest cart data is stored only in the session and not persisted.

        Expected Result:
            After clearing cookies and refreshing, the cart is empty.
        """
        # fixture goes to home page and adds first product to cart
        self.header.wait_until_cart_item_count(1)

        # clear cookies and refresh browser
        self.driver.delete_all_cookies()
        self.driver.refresh()

        # verify cart is now empty
        self.home_page.go_to_home_page()
        self.header.wait_until_cart_item_count(0)

        self.header.click_on_cart_on_right_header()

        # verify empty cart message on cart page
        self.cart_page.verify_empty_cart()