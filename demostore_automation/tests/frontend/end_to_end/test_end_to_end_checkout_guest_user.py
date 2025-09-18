"""End-to-End Checkout Tests.

This module validates the checkout flow for both guest and registered users.
It ensures that:
    * Products can be added to the cart.
    * Coupons are applied successfully.
    * Orders can be placed through the checkout page.
    * Orders appear in the account order history for registered users.
"""
import pytest
from demostore_automation.src.pages.HomePage import HomePage
from demostore_automation.src.pages.CartPage import CartPage
from demostore_automation.src.pages.Header import Header
from demostore_automation.src.pages.CheckoutPage import CheckoutPage
from demostore_automation.src.pages.MyAccountSignedInPage import MyAccountSignedInPage
from demostore_automation.src.pages.MyAccountSignedOutPage import MyAccountSignedOutPage
from demostore_automation.src.pages.OrderReceivedPage import OrderReceivedPage
from demostore_automation.src.configs.MainConfigs import MainConfigs
from demostore_automation.src.utilities.genericUtilities import generate_random_email_and_password

pytestmark = [pytest.mark.feregression, pytest.mark.end_to_end]

@pytest.mark.parametrize(
    "user_type",
    [pytest.param("guest_user", marks=[pytest.mark.efe123, pytest.mark.fesmoke, pytest.mark.smoke]),
    pytest.param("registered_user",  marks=[pytest.mark.efe124])
    ]
)


@pytest.mark.usefixtures("init_driver")
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
        # create objects
        my_acc_so = MyAccountSignedOutPage(self.driver)
        my_acc_si = MyAccountSignedInPage(self.driver)
        home_page = HomePage(self.driver)
        header = Header(self.driver)
        cart_page = CartPage(self.driver)
        checkout_page = CheckoutPage(self.driver)
        order_received = OrderReceivedPage(self.driver)

        if user_type == 'registered_user': # create a registered user
            my_acc_so.go_to_my_account()
            registered_email = generate_random_email_and_password()['email']
            my_acc_so.input_register_email(registered_email)
            my_acc_so.input_register_password(generate_random_email_and_password()['password'])
            my_acc_so.click_register_button()

        # go to home page
        home_page.go_to_home_page()

        # add item to cart
        home_page.click_first_add_to_cart_button()

        # make sure the cart is updated before going to cart
        header.wait_until_cart_item_count(1)

        # go to cart
        header.click_on_cart_on_right_header()

        # verify there are items in the cart
        product_names = cart_page.get_all_product_names_in_cart()
        assert len(product_names) == 1, f"Expected 1 product in cart but found {len(product_names)}"

        #  apply coupon
        cart_page.click_apply_coupon_arrow()
        coupon_code = MainConfigs.get_coupon_code('FREE_COUPON')
        cart_page.apply_coupon(coupon_code)
        cart_page.verify_order_total_is_0()

        # proceed to checkout
        cart_page.click_on_proceed_to_checkout()

        # fill in checkout form
        if user_type == 'registered_user':
            checkout_page.fill_in_billing_info()
        else:
            checkout_page.fill_in_billing_info()

        # submit
        checkout_page.click_place_order()
        checkout_page.click_place_order()

        # verify order is placed
        order_received.verify_order_received_page_loaded()
        order_number = order_received.get_order_number()

        print('********')
        print(order_number)
        print('********')

        # if registered user, go to orders page to verify order exists
        if user_type == 'registered':
            my_acc_so.go_to_my_account()
            my_acc_si.go_to_orders()
            my_acc_si.verify_order_number_exists_in_orders(expected_order_number=order_number)

