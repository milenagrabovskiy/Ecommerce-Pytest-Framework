
from demostore_automation.src.pages.locators.MyAccountSignedOutPageLocators import MyAccountSignedOutPageLocators

from demostore_automation.src.selenium_extended.SeleniumExtended import SeleniumExtended

from demostore_automation.src.configs.MainConfigs import MainConfigs

class MyAccountSignedOutPage(MyAccountSignedOutPageLocators):

    endpoint = '/my-account/'


    def __init__(self, driver):
        self.driver = driver
        self.sl = SeleniumExtended(self.driver)

    def go_to_my_account(self):
        base_url = MainConfigs.get_base_url()
        my_account_url = base_url + self.endpoint
        self.driver.get(my_account_url)

    def input_login_username(self, username):
        self.sl.wait_and_input_text(self.LOGIN_USER_NAME, username)

    def input_login_password(self, password):
        self.sl.wait_and_input_text(self.LOGIN_USER_PASSWORD, password)

    def click_login_button(self):
        self.sl.wait_and_click(self.LOGIN_BTN)

    def wait_until_error_is_displayed(self, exp_err):
        self.sl.wait_until_element_contains_text(self.ERRORS_UL, exp_err)

    def input_register_email(self, email):
        self.sl.wait_and_input_text(self.REGISTER_EMAIL, email)

    def input_register_password(self, password):
        self.sl.wait_and_input_text(self.REGISTER_PASSWORD, password)

    def click_register_button(self):
        self.sl.wait_and_click(self.REGISTER_BTN)

    def is_register_btn_enabled(self):
        return self.sl.wait_until_element_is_visible(self.REGISTER_BTN).is_enabled()

    def click_on_lost_password_link(self):
        self.sl.wait_and_click(self.LOST_PASSWORD_LINK)

    def verify_on_password_reset_page(self):
        self.sl.wait_until_element_contains_text(self.LOST_PASSWORD_HEADER, 'Lost password')
        self.sl.wait_until_element_is_visible(self.LOST_PASSWORD_EMAIL)
        self.sl.wait_until_element_is_visible(self.RESET_PASSWORD_BTN)

    def input_email_to_reset_password(self, email):
        self.sl.wait_and_input_text(self.LOST_PASSWORD_EMAIL, email)
        self.sl.wait_and_click(self.RESET_PASSWORD_BTN)

    def verify_wrong_email_alert_displayed(self):
        self.sl.wait_until_element_contains_text(self.INVALID_EMAIL_ALERT, 'Invalid username or email.')

    def verify_password_reset_sent(self):
        self.sl.wait_until_element_contains_text(self.PASSWORD_RESET_SENT_MSG, 'Password reset email has been sent.')