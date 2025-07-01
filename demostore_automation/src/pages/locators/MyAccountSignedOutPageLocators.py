
from selenium.webdriver.common.by import By

class MyAccountSignedOutPageLocators:

    LOGIN_USER_NAME = (By.ID, 'username')
    LOGIN_USER_PASSWORD = (By.ID, 'password')
    LOGIN_BTN = (By.CSS_SELECTOR, 'button.woocommerce-button[name="login"]')

    ERRORS_UL = (By.CSS_SELECTOR, 'ul.woocommerce-error')

    REGISTER_EMAIL = (By.ID, 'reg_email')
    REGISTER_PASSWORD = (By.ID, 'reg_password')
    REGISTER_BTN = (By.CSS_SELECTOR, 'button[name="register"][value="Register"]')