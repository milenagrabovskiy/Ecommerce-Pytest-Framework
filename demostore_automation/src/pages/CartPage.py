from demostore_automation.src.pages.Header import Header
from demostore_automation.src.selenium_extended.SeleniumExtended import SeleniumExtended
from demostore_automation.src.pages.locators.CartPageLocators import CartPageLocators
from demostore_automation.src.configs.MainConfigs import MainConfigs


class CartPage(CartPageLocators):

    endpoint = '/cart'

    def __init__(self, driver):
        self.driver = driver
        self.sl = SeleniumExtended(driver)

    def go_to_cart_page(self):
        base_url = MainConfigs.get_base_url()
        cart_url = base_url + self.endpoint
        self.driver.get(cart_url)

    def get_all_product_names_in_cart(self):

        product_name_elements = self.sl.wait_and_get_elements(self.PRODUCT_NAMES_IN_CART)
        product_names = [i.text for i in product_name_elements]
        # product_names = []
        # for i in product_name_elements:
        #     product_names.append(i.text)
        return product_names

    def input_coupon(self, coupon_code):
        self.sl.wait_and_input_text(self.COUPON_FIELD, str(coupon_code))

    def click_apply_coupon(self):
        self.sl.wait_and_click(self.APPLY_COUPON_BTN)

    def click_apply_coupon_arrow(self):
        self.sl.wait_and_click(self.APPLY_COUPON_ARROW)

    def apply_coupon(self, coupon_code):
        self.input_coupon(coupon_code)
        self.click_apply_coupon()

    def remove_coupon(self):
        self.sl.wait_and_click(self.REMOVE_COUPON_BTN)

    def verify_expired_coupon_error(self):
        self.sl.wait_until_element_contains_text(self.EXPIRED_COUPON_ERROR, 'This coupon has expired.')

    def get_order_total(self):
        return self.sl.wait_and_get_text(self.CART_TOTAL)

    def verify_order_total_is_0(self):
        self.sl.wait_until_element_contains_text(self.CART_TOTAL, '$0.00')

    def verify_order_total(self, expected_total):
        self.sl.wait_until_element_contains_text(self.CART_TOTAL, expected_total)

    def click_on_proceed_to_checkout(self):
        self.sl.wait_and_click(self.PROCEED_TO_CHECKOUT_BTN)

    def verify_sale_badge_displayed(self):
        self.sl.wait_until_element_contains_text(self.SAVE_BADGE, 'SAVE')
        
    def remove_product(self):
        self.sl.wait_and_click(self.REMOVE_PRODUCT_BTN)

    def get_qty_of_product(self):
        qty_field = self.sl.wait_until_element_is_visible(self.PRODUCT_QTY)
        actual_qty = int(qty_field.get_attribute("value"))
        return actual_qty

    def verify_empty_cart(self):
        self.sl.wait_until_element_contains_text(self.EMPTY_CART, 'Your cart is currently empty!')