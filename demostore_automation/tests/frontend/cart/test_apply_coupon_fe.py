"""Frontend cart coupon tests

Validates behavior when applying coupons in the shopping cart, including:
- Adding items to the cart
- Applying coupons
- Verifying order total
"""

import pytest
from demostore_automation.src.pages.HomePage import HomePage
from demostore_automation.src.pages.CartPage import CartPage
from demostore_automation.src.pages.Header import Header
from demostore_automation.src.configs.MainConfigs import MainConfigs

pytestmark = [pytest.mark.feregression, pytest.mark.fesmoke, pytest.mark.cart]


@pytest.mark.usefixtures("init_driver")
class TestApplyCouponNegFE:
    """Tests for applying coupons in the front-end cart with negative scenarios.

    This test class focuses on validating the behavior of the cart when applying
    coupons.
    """
    def test_apply_coupon_neg_fe(self):
        """Test applying a 50% off coupon to a single cart item.

        Assertions:
            - The cart contains exactly one product.
            - The order total after applying the coupon matches the expected discounted value.

        Raises:
            AssertionError: If the cart item count or order total does not match expectations.
        """
        home_page = HomePage(self.driver)
        header = Header(self.driver)
        cart_page = CartPage(self.driver)

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
        coupon_code = MainConfigs.get_coupon_code('50_OFF')


        cart_page.apply_coupon(coupon_code)
        cart_page.verify_order_total(expected_total='5.63')