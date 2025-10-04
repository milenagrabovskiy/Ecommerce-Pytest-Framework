
from selenium.webdriver.common.by import By

class MyAccountSignedInPageLocators:

    LEFT_NAV_LOGOUT_BTN = (By.CSS_SELECTOR, 'li.woocommerce-MyAccount-navigation-link--customer-logout a')
    ORDERS = (By.CSS_SELECTOR, 'a[href="http://dev.bootcamp.store.supersqa.com/my-account/orders/"]')
    LOGOUT_LINK = (By.XPATH, '//*[@id="post-9"]/div/div/div/p[1]/a')
    SIDE_NAVIGATION = (By.XPATH, '//*[@id="post-9"]/div/div/nav/ul')
    ACCOUNT_DETAILS = (By.CSS_SELECTOR, 'a[href="http://dev.bootcamp.store.supersqa.com/my-account/edit-account/"]')
    #EMAIL = (By.ID, 'account_email')
    EMAIL = (By.CSS_SELECTOR, 'input.woocommerce-Input.woocommerce-Input--email.input-text')