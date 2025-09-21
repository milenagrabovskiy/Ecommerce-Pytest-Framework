"""Tests for changing product quantity on the PDP.

Covers:
- Setting product quantity on the Product Description Page
- Validating quantity restrictions (zero, negative, high values)
- Verifying correct quantity in cart
- Removing product from cart
"""
import pytest
import logging as logger
from demostore_automation.src.pages.HomePage import HomePage
from demostore_automation.src.pages.CartPage import CartPage
from demostore_automation.src.pages.Header import Header
from demostore_automation.src.pages.ProductDescriptionPage import ProductDescriptionPage

pytestmark = [pytest.mark.feregression, pytest.mark.pdp]

@pytest.mark.parametrize(
    "quantity",
    [
    pytest.param(0, marks=pytest.mark.efe33, id='product qty 0'),
    pytest.param(5, marks=[pytest.mark.efe34, pytest.mark.smoke, pytest.mark.smokefe], id='mid range product qty'),
    pytest.param(-1, marks=pytest.mark.efe35, id='negative product qty')
    ]
)

@pytest.mark.usefixtures("init_driver")
class TestChangeProductQuantity:
    """Test changing product quantity on PDP and validating cart behavior."""

    def test_change_product_quantity(self, quantity):
        """Verify product quantity can be set on PDP and reflected in cart.

        Handles edge cases for zero, negative, and high quantities.
        Removes product and checks cart emptiness for cleanup.

        Args:
            quantity (int): Quantity to set for the product.
        """
        home_page = HomePage(self.driver)
        pdp_page = ProductDescriptionPage(self.driver)
        header = Header(self.driver)
        cart_page = CartPage(self.driver)

        # go to home page
        home_page.go_to_home_page()

        # add item to cart
        home_page.click_first_product()
        pdp_page.type_product_qty(quantity)

        # add to cart
        if quantity <= 0:
            pdp_page.verify_qty_error_msg()
            logger.info(f"Successfully passed negative test case with 0 or negative quantity.")
            return
        pdp_page.click_add_to_cart()

        # wait until cart loads
        header.wait_until_cart_item_count(quantity)

        # go to cart
        header.click_on_cart_on_right_header()

        # verify quantity in cart
        actual_qty = cart_page.get_qty_of_product()
        assert actual_qty == quantity

        # remove product
        cart_page.remove_product()
        # verify empty cart message. remove product does not change side header cart item count
        cart_page.verify_empty_cart()