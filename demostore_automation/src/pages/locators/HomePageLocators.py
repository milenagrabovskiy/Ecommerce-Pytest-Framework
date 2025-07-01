from selenium.webdriver.common.by import By

class HomePageLocators:

    ADD_TO_CART_BTN = (By.CSS_SELECTOR, 'li.product a.button.add_to_cart_button')
    PRODUCT = (By.CSS_SELECTOR, 'ul.products li.product')

    PAGE_HEADING = (By.CSS_SELECTOR, 'header.woocommerce-products-header h1.page-title')