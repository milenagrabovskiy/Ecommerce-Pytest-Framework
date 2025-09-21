from selenium.webdriver.common.by import By

class HomePageLocators:

    ADD_TO_CART_BTN = (By.CSS_SELECTOR, 'li.product a.button.add_to_cart_button')
    PRODUCT = (By.CSS_SELECTOR, 'ul.products li.product')

    PAGE_HEADING = (By.CSS_SELECTOR, 'header.woocommerce-products-header h1.page-title')

    SEARCH_BAR_FIELD = (By.ID, 'woocommerce-product-search-field-0')

    PRODUCT_NAMES = (By.CSS_SELECTOR, 'h2.woocommerce-loop-product__title')

    NO_PRODUCTS_MSG_LOCATOR = (By.CSS_SELECTOR, 'div.woocommerce-info')
