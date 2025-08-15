
from selenium.webdriver.common.by import By

class CartPageLocators:

    PRODUCT_NAMES_IN_CART = (By.CSS_SELECTOR, 'a.wc-block-components-product-name')
    APPLY_COUPON_ARROW = (By.CSS_SELECTOR, 'button.wc-block-components-panel__button')
    COUPON_FIELD = (By.ID, 'wc-block-components-totals-coupon__input-0')
    APPLY_COUPON_BTN = (By.CSS_SELECTOR, 'button.wc-block-components-button.wc-block-components-totals-coupon__button')
    CART_TOTAL = (By.CSS_SELECTOR, 'div.wc-block-components-totals-item__value')
    #PROCEED_TO_CHECKOUT_BTN = (By.CSS_SELECTOR, 'a.wc-block-components-button.wp-element-button.wc-block-cart__submit-button')
    PROCEED_TO_CHECKOUT_BTN = (By.CSS_SELECTOR, "a[href*='/checkout/']")