
from selenium.webdriver.common.by import By

class HeaderLocators:

    CART_RIGHT_HEADER = (By.ID, 'site-header-cart')
    CART_ITEM_COUNT = (By.CSS_SELECTOR, 'li a.cart-contents span.count')
    MENU_ITEMS = (By.CSS_SELECTOR, 'div.menu ul.nav-menu li')
    DEMO_ECOM_STORE_HEADER = (By.CSS_SELECTOR, 'div.beta.site-title')
    DEMO_ECOM_STORE_HEADER_LINK = (By.CSS_SELECTOR, 'a[href="http://dev.bootcamp.store.supersqa.com/"]')