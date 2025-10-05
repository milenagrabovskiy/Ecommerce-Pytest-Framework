
from selenium.webdriver.common.by import By

class MyAccountSignedInPageLocators:

    LEFT_NAV_LOGOUT_BTN = (By.CSS_SELECTOR, 'li.woocommerce-MyAccount-navigation-link--customer-logout a')
    ORDERS = (By.CSS_SELECTOR, 'a[href="http://dev.bootcamp.store.supersqa.com/my-account/orders/"]')
    #LOGOUT_LINK = (By.XPATH, '//*[@id="post-9"]/div/div/div/p[1]/a')
    LOGOUT_LINK = (By.XPATH, '//*[@id="post-9"]/div/div/nav/ul/li[6]/a')
    SIDE_NAVIGATION = (By.XPATH, '//*[@id="post-9"]/div/div/nav/ul')
    ACCOUNT_DETAILS = (By.CSS_SELECTOR, 'a[href="http://dev.bootcamp.store.supersqa.com/my-account/edit-account/"]')
    ACC_DETAILS_HEADER = (By.CSS_SELECTOR, 'h1.entry-title')
    MY_ACCOUNT_HEADER = (By.CSS_SELECTOR, 'h1.entry-title')
    #EMAIL = (By.ID, 'account_email')
    EMAIL = (By.CSS_SELECTOR, 'input.woocommerce-Input.woocommerce-Input--email.input-text')
    FIRST_NAME = (By.ID, 'account_first_name')
    LAST_NAME = (By.ID, 'account_last_name')
    PASSWORD_FIELD = (By.ID, 'password_current')
    NEW_PASSWORD_FIELD = (By.ID, 'password_1')
    CONFIRM_NEW_PASSWORD_FIELD = (By.ID, 'password_2')
    SAVE_CHANGES_BTN = (By.CSS_SELECTOR, 'button.woocommerce-Button.button')
    CHANGE_PASSWORD_SUCCESS_MSG = (By.CSS_SELECTOR, 'div.woocommerce div.woocommerce-message')
    DASHBOARD = (By.CSS_SELECTOR, 'li.woocommerce-MyAccount-navigation-link.woocommerce-MyAccount-navigation-link')