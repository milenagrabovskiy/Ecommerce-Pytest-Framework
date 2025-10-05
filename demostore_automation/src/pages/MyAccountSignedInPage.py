from selenium.webdriver.common.by import By

from demostore_automation.src.selenium_extended.SeleniumExtended import SeleniumExtended
from demostore_automation.src.pages.locators.MyAccountSignedInPageLocators import MyAccountSignedInPageLocators


class MyAccountSignedInPage(MyAccountSignedInPageLocators):

    def __init__(self, driver):
        self.sl = SeleniumExtended(driver)

    def get_my_account_header(self):
        return self.sl.wait_and_get_text(self.MY_ACCOUNT_HEADER)

    def verify_user_is_signed_in(self):
        """
        Verifies user is signed in by checking the 'Log Out' button is visible
        on the left navigation bar.
        :return:
        """
        self.sl.wait_until_element_is_visible(self.LEFT_NAV_LOGOUT_BTN)


    def is_user_signed_in(self):
        """Return True if logout link is visible, otherwise False."""
        try:
            return self.driver.find_element(*self.LEFT_NAV_LOGOUT_BTN).is_displayed()
        except:
            return False

    def go_to_orders(self):
        self.sl.wait_and_click(self.ORDERS)


    def verify_order_number_exists_in_orders(self, expected_order_number):
        order_locator = (By.CSS_SELECTOR, f'a[href="http://dev.bootcamp.store.supersqa.com/my-account/view-order/{expected_order_number}/"]')
        self.sl.wait_until_element_is_visible(order_locator)

    def click_logout(self):
        self.sl.wait_and_click(self.LOGOUT_LINK)

    def get_side_navigation_menu(self):
        self.sl.wait_until_element_is_visible(self.SIDE_NAVIGATION)

    def go_to_account_details(self):
        self.sl.wait_and_click(self.ACCOUNT_DETAILS)
        return self.sl.wait_and_get_text(self.ACC_DETAILS_HEADER)

    def get_my_acc_details_email(self):
        self.sl.wait_until_element_is_visible(self.EMAIL)
        email_input = self.sl.wait_and_get_elements(self.EMAIL)[0]
        return email_input.get_attribute("value")

    def input_first_name(self, f_name):
        self.sl.wait_and_input_text(self.FIRST_NAME, f_name)

    def input_last_name(self, l_name):
        self.sl.wait_and_input_text(self.LAST_NAME, l_name)

    def input_current_password(self, current_password):
        self.sl.wait_and_input_text(self.PASSWORD_FIELD, current_password)

    def input_new_password(self, new_password):
        self.sl.wait_and_input_text(self.NEW_PASSWORD_FIELD, new_password)

    def confirm_new_password(self, new_password):
        self.sl.wait_and_input_text(self.CONFIRM_NEW_PASSWORD_FIELD, new_password)

    def click_on_save_changes_btn(self):
        self.sl.wait_and_click(self.SAVE_CHANGES_BTN)

    def get_password_changed_success_msg(self):
        return self.sl.wait_and_get_text(self.CHANGE_PASSWORD_SUCCESS_MSG)

    def go_to_dashboard(self):
        self.sl.wait_and_click(self.DASHBOARD)