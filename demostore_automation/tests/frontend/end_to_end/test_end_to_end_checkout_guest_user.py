"""End-to-End Checkout Tests.

This module validates the checkout flow for both guest and registered users.
It ensures that:
    * Products can be added to the cart.
    * Coupons are applied successfully.
    * Orders can be placed through the checkout page.
    * Orders appear in the account order history for registered users.
    * All page objects (HomePage, CartPage, CheckoutPage, etc.) are initialized
      via a class-scoped fixture (`setup_fixture`) and available via `self`.
"""
import pytest
import logging as logger
from demostore_automation.conftest import init_driver
from demostore_automation.src.pages.HomePage import HomePage
from demostore_automation.src.pages.CartPage import CartPage
from demostore_automation.src.pages.Header import Header
from demostore_automation.src.pages.CheckoutPage import CheckoutPage
from demostore_automation.src.pages.MyAccountSignedInPage import MyAccountSignedInPage
from demostore_automation.src.pages.MyAccountSignedOutPage import MyAccountSignedOutPage
from demostore_automation.src.pages.OrderReceivedPage import OrderReceivedPage
from demostore_automation.src.configs.MainConfigs import MainConfigs
from demostore_automation.src.utilities.genericUtilities import generate_random_email_and_password
from demostore_automation.src.api_helpers.OrdersAPIHelper import OrdersAPIHelper


@pytest.fixture(scope='class')
def setup_fixture(request):
    request.cls.my_acc_so = MyAccountSignedOutPage(request.cls.driver)
    request.cls.my_acc_si = MyAccountSignedInPage(request.cls.driver)
    request.cls.home_page = HomePage(request.cls.driver)
    request.cls.header = Header(request.cls.driver)
    request.cls.cart_page = CartPage(request.cls.driver)
    request.cls.checkout_page = CheckoutPage(request.cls.driver)
    request.cls.order_received = OrderReceivedPage(request.cls.driver)


pytestmark = [pytest.mark.feregression, pytest.mark.end_to_end]

@pytest.mark.parametrize(
    "user_type",
    [pytest.param("guest_user", marks=[pytest.mark.efe123, pytest.mark.fesmoke, pytest.mark.smoke]),
    pytest.param("registered_user",  marks=[pytest.mark.efe124])
    ]
)


@pytest.mark.usefixtures("init_driver", "setup_fixture")
class TestEndToEndCheckout:
    """End-to-end checkout test suite.

    This class contains parameterized tests for guest and registered users
    to validate the checkout flow.

    The flow covers:
        * Account creation (for registered users).
        * Adding products to the cart.
        * Applying coupons.
        * Completing checkout and verifying order confirmation.
        * For registered users, confirming that the order appears in order history.
    """
    @pytest.mark.tcid33
    @pytest.mark.pioneertcid3
    def test_end_to_end_checkout(self, user_type):
        """Validate end-to-end checkout for guest and registered users.

        This test relies on the `setup_fixture` class-scoped fixture, which initializes
        all required page objects.

        Args:
            user_type (str): The type of user to test with. Can be:
                * "guest_user" – goes through checkout without creating an account.
                * "registered_user" – registers a new account and verifies order history.

        Asserts:
            * A product can be successfully added to the cart.
            * The coupon is applied and the order total is updated.
            * An order number is generated upon successful checkout.
            * For registered users, the order number appears in account history.
        """
        if user_type == 'registered_user': # create a registered user
            self.my_acc_so.go_to_my_account()
            self.registered_email = generate_random_email_and_password()['email']
            self.my_acc_so.input_register_email(self.registered_email)
            self.my_acc_so.input_register_password(generate_random_email_and_password()['password'])
            self.my_acc_so.click_register_button()

        # go to home page
        self.home_page.go_to_home_page()

        # add item to cart
        self.home_page.click_first_add_to_cart_button()

        # make sure the cart is updated before going to cart
        self.header.wait_until_cart_item_count(1)

        # go to cart
        self.header.click_on_cart_on_right_header()

        # verify there are items in the cart
        product_names = self.cart_page.get_all_product_names_in_cart()
        assert len(product_names) == 1, f"Expected 1 product in cart but found {len(product_names)}"

        #  apply coupon
        self.cart_page.click_apply_coupon_arrow()
        coupon_code = MainConfigs.get_coupon_code('FREE_COUPON')
        self.cart_page.apply_coupon(coupon_code)
        self.cart_page.verify_order_total_is_0()

        # proceed to checkout
        self.cart_page.click_on_proceed_to_checkout()

        # fill in checkout form
        if user_type == 'registered_user':
            self.checkout_page.fill_in_billing_info()
        else:
            self.checkout_page.fill_in_billing_info()

        # submit
        self.checkout_page.click_place_order()
        self.checkout_page.click_place_order()

        # verify order is placed
        self.order_received.verify_order_received_page_loaded()
        order_number = self.order_received.get_order_number()

        logger.info(f"Created order with order number: {order_number}")

        # if registered user, go to orders page to verify order exists
        if user_type == 'registered_user':
            self.my_acc_so.go_to_my_account()
            self.my_acc_si.go_to_orders()
            self.my_acc_si.verify_order_number_exists_in_orders(expected_order_number=order_number)

        # teardown
        try:
            OrdersAPIHelper().call_delete_order(order_id=order_number)
        except Exception as e:
            logger.error(f"ERROR. Could not delete order with id: {order_number}. Error message: {e}")

        logger.info(f"Successfully deleted order with order_id: {order_number}")