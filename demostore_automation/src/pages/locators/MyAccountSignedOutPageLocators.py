
from selenium.webdriver.common.by import By

class MyAccountSignedOutPageLocators:

    LOGIN_USER_NAME = (By.ID, 'username')
    LOGIN_USER_PASSWORD = (By.ID, 'password')
    LOGIN_BTN = (By.CSS_SELECTOR, 'button.woocommerce-button[name="login"]')

    ERRORS_UL = (By.CSS_SELECTOR, 'ul.woocommerce-error')

    REGISTER_EMAIL = (By.ID, 'reg_email')
    REGISTER_PASSWORD = (By.ID, 'reg_password')
    REGISTER_BTN = (By.CSS_SELECTOR, 'button[name="register"][value="Register"]')

    LOST_PASSWORD_LINK = (By.CSS_SELECTOR, 'a[href="http://dev.bootcamp.store.supersqa.com/my-account/lost-password/"]')
    LOST_PASSWORD_EMAIL = (By.CSS_SELECTOR, 'input.woocommerce-Input.woocommerce-Input--text.input-text')
    RESET_PASSWORD_BTN = (By.CSS_SELECTOR, 'button.woocommerce-Button.button')
    LOST_PASSWORD_HEADER = (By.CSS_SELECTOR, 'h1.entry-title')
    INVALID_EMAIL_ALERT = (By.CSS_SELECTOR, 'ul.woocommerce-error')
    PASSWORD_RESET_SENT_MSG = (By.CSS_SELECTOR, 'div.woocommerce-message')