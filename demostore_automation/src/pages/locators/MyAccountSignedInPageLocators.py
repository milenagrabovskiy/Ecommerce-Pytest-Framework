
from selenium.webdriver.common.by import By

class MyAccountSignedInPageLocators:

    LEFT_NAV_LOGOUT_BTN = (By.CSS_SELECTOR, 'li.woocommerce-MyAccount-navigation-link--customer-logout a')
    ORDERS = (By.CSS_SELECTOR, 'a[href="http://dev.bootcamp.store.supersqa.com/my-account/orders/"]')