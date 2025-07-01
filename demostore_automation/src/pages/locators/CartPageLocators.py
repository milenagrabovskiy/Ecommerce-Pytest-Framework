
from selenium.webdriver.common.by import By

class CartPageLocators:

    PRODUCT_NAMES_IN_CART = (By.CSS_SELECTOR, 'tr.cart_item td.product-name')

    COUPON_FIELD = (By.ID, 'coupon_code')
    APPLY_COUPON_BTN = (By.CSS_SELECTOR, 'button[name="apply_coupon"]')

    PROCEED_TO_CHECKOUT_BTN = (By.CSS_SELECTOR, 'a.checkout-button')