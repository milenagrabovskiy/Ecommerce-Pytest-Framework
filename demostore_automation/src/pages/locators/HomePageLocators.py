from selenium.webdriver.common.by import By

class HomePageLocators:

    ADD_TO_CART_BTN = (By.CSS_SELECTOR, 'li.product a.button.add_to_cart_button')
    PRODUCT = (By.CSS_SELECTOR, 'ul.products li.product')

    PAGE_HEADING = (By.CSS_SELECTOR, 'header.woocommerce-products-header h1.page-title')

    SEARCH_BAR_FIELD = (By.ID, 'woocommerce-product-search-field-0')

    PRODUCT_NAMES = (By.CSS_SELECTOR, 'h2.woocommerce-loop-product__title')

    NO_PRODUCTS_MSG_LOCATOR = (By.CSS_SELECTOR, 'div.woocommerce-info')

    FIRST_PRODUCT = (By.XPATH, '//*[@id="main"]/ul/li[1]/a[1]/h2' )

    SORTING_MENU = (By.CSS_SELECTOR, 'select.orderby, select.orderby')

    PRICES = (By.CSS_SELECTOR, 'span.woocommerce-Price-amount.amount')

    PRODUCT_IMAGES = (By.CSS_SELECTOR, 'li.product img.attachment-woocommerce_thumbnail.size-woocommerce_thumbnail')