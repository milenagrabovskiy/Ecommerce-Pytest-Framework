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
from demostore_automation.src.pages.ProductDescriptionPage import ProductDescriptionPage

pytestmark = [pytest.mark.feregression, pytest.mark.fesmoke, pytest.mark.prod]

@pytest.mark.parametrize(
    "quantity",
    [
    pytest.param(5),
    pytest.param(0)
    ]
)

@pytest.mark.usefixtures("init_driver")
class TestChangeProductQuantity:

    def test_change_product_quantity(self):

        home_page = HomePage(self.driver)
        pdp_page = ProductDescriptionPage(self.driver)
        header = Header(self.driver)
        cart_page = CartPage(self.driver)

        # go to home page
        home_page.go_to_home_page()

        # add item to cart
        home_page.click_first_product()
        pdp_page.type_product_qty(5)

        # add to cart
        pdp_page.click_add_to_cart()

        # wait until cart loads
        header.wait_until_cart_item_count(5)

        # go to cart
        header.click_on_cart_on_right_header()

        # verify quantity in cart
        actual_qty = cart_page.get_qty_of_product()
        assert actual_qty == 5, f"Wrong product qty in cart. Actual: {actual_qty}, Expected: 5"

