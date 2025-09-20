
import time
import pytest
import logging as logger
from demostore_automation.src.pages.HomePage import HomePage
from demostore_automation.src.pages.CartPage import CartPage
from demostore_automation.src.pages.Header import Header
from demostore_automation.src.configs.MainConfigs import MainConfigs


# @pytest.fixture(scope='class')
# def setup(request):
#     request.cls.home_page = HomePage(request.cls.driver)
#     request.cls.header = Header(request.cls.driver)
#     request.cls.cart_page = CartPage(request.cls.driver)
#
#     # go to homepage
#     request.cls.home_page.go_to_home_page()
#     # add item to cart
#
#     request.cls.home_page.click_first_add_to_cart_button()
#
#     # make sure the cart is updated before going to cart
#     request.cls.header.wait_until_cart_item_count(1)
#
#     # go to cart
#     request.cls.header.click_on_cart_on_right_header()
#
#     # verify there are items in the cart
#     product_names = request.cls.cart_page.get_all_product_names_in_cart()
#     assert len(product_names) == 1, f"Expected 1 product in cart but found {len(product_names)}"
#

pytestmark = [pytest.mark.feregression, pytest.mark.fesmoke, pytest.mark.cart]

@pytest.mark.parametrize(
    "coupon_type",
    [pytest.param("50_OFF"),
    pytest.param("ZERO_OFF"),
    pytest.param("EXPIRED_COUPON")
    ]
)



@pytest.mark.usefixtures("init_driver")
class TestApplyCouponFE:

    def test_apply_coupon_fe(self, coupon_type):
        home_page = HomePage(self.driver)
        header = Header(self.driver)
        cart_page = CartPage(self.driver)

        # go to homepage
        home_page.go_to_home_page()

        # add item to cart
        home_page.click_first_add_to_cart_button()

        # make sure the cart is updated before going to cart
        #header.wait_until_cart_item_count(1)

        # go to cart
        header.click_on_cart_on_right_header()

        # verify there are items in the cart
        # product_names = cart_page.get_all_product_names_in_cart()
        # assert len(product_names) == 1, f"Expected 1 product in cart but found {len(product_names)}"
        # get total before coupon
        total_before = float(cart_page.get_order_total().strip('$'))

        #  apply coupon
        cart_page.click_apply_coupon_arrow()
        coupon_code = MainConfigs.get_coupon_code(coupon_type)
        cart_page.apply_coupon(coupon_code)

        if coupon_type == '50_OFF':
            expected_total = 5.63

        elif coupon_type == 'ZERO_OFF':
            expected_total = total_before

        elif coupon_type == 'EXPIRED_COUPON':
            cart_page.verify_expired_coupon_error() # error message displayed for expired coupon
            expected_total = total_before

        expected_total = round(expected_total, 2)
        total_actual = round(float(cart_page.get_order_total().strip('$')), 2)

        # assert total is equal to expected
        assert total_actual == expected_total, f"Expected total {expected_total}, Actual: {total_actual}"
        cart_page.verify_order_total(f"{expected_total:.2f}")

        if coupon_type != 'EXPIRED_COUPON':
            cart_page.remove_coupon()
        cart_page.remove_product()

