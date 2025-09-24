"""Frontend cart coupon negative tests.

Tests behavior of the cart when applying invalid or zero-value coupons, including:
- Applying a zero-discount coupon
- Applying an expired coupon
- Verifying that order totals remain unchanged and error messages are shown
"""
import pytest
from demostore_automation.src.pages.HomePage import HomePage
from demostore_automation.src.pages.CartPage import CartPage
from demostore_automation.src.pages.Header import Header
from demostore_automation.src.configs.MainConfigs import MainConfigs

pytestmark = [pytest.mark.feregression, pytest.mark.cart, pytest.mark.coupon]

@pytest.mark.parametrize(
    "coupon_type",
    [
    pytest.param("ZERO_OFF", marks=pytest.mark.efe37, id='add 0% off coupon'),
    pytest.param("EXPIRED_COUPON", marks=pytest.mark.efe38, id='add expired coupon')
    ]
)

@pytest.mark.usefixtures("init_driver")
class TestApplyCouponNegFE:
    """Tests negative scenarios for applying coupons in the frontend cart."""

    def test_apply_coupon_neg_fe(self, coupon_type):
        """Apply a coupon and verify order total or error message.

        Args:
            coupon_type (str): Type of coupon to apply (e.g., ZERO_OFF, EXPIRED_COUPON)
        """
        home_page = HomePage(self.driver)
        header = Header(self.driver)
        cart_page = CartPage(self.driver)

        # go to homepage
        home_page.go_to_home_page()

        # add item to cart
        home_page.click_first_add_to_cart_button()

        # go to cart
        header.click_on_cart_on_right_header()

        # get total before coupon
        total_before = float(cart_page.get_order_total().strip('$'))

        #  apply coupon
        cart_page.click_apply_coupon_arrow()
        coupon_code = MainConfigs.get_coupon_code(coupon_type)
        cart_page.apply_coupon(coupon_code)

        if coupon_type == 'ZERO_OFF':
            expected_total = total_before

        elif coupon_type == 'EXPIRED_COUPON':
            cart_page.verify_expired_coupon_error() # error message displayed for expired coupon
            expected_total = total_before

        expected_total = round(expected_total, 2)
        total_actual = round(float(cart_page.get_order_total().strip('$')), 2)

        # assert total is equal to expected
        assert total_actual == expected_total, f"Expected total {expected_total}, Actual: {total_actual}"
        cart_page.verify_order_total(f"{expected_total:.2f}")

        # clean up cart
        cart_page.remove_product()
        cart_page.verify_empty_cart()