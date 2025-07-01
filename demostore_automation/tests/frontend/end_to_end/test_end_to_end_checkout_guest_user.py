
import pytest

from demostore_automation.src.pages.HomePage import HomePage
from demostore_automation.src.pages.CartPage import CartPage
from demostore_automation.src.pages.Header import Header
from demostore_automation.src.pages.CheckoutPage import CheckoutPage
from demostore_automation.src.pages.OrderReceivedPage import OrderReceivedPage
from demostore_automation.src.configs.MainConfigs import MainConfigs


pytestmark = [pytest.mark.feregression, pytest.mark.fesmoke, pytest.mark.end_to_end]




@pytest.mark.usefixtures("init_driver")
class TestEndToEndCheckoutGuestUser:

    @pytest.mark.tcid33
    @pytest.mark.pioneertcid3
    def test_end_to_end_checkout_guest_user(self):
        # create objects
        home_page = HomePage(self.driver)
        header = Header(self.driver)
        cart_page = CartPage(self.driver)
        checkout_page = CheckoutPage(self.driver)
        order_received = OrderReceivedPage(self.driver)

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
        coupon_code = MainConfigs.get_coupon_code('FREE_COUPON')
        cart_page.apply_coupon(coupon_code)

        # proceed to checkout
        cart_page.click_on_proceed_to_checkout()

        # fill in checkout form
        checkout_page.fill_in_billing_info()

        # submit
        checkout_page.click_place_order()

        # verify order is placed
        order_received.verify_order_received_page_loaded()
        order_number = order_received.get_order_number()

        print('********')
        print(order_number)
        print('********')

