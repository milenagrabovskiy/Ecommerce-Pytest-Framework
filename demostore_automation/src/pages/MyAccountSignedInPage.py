
from demostore_automation.src.selenium_extended.SeleniumExtended import SeleniumExtended
from demostore_automation.src.pages.locators.MyAccountSignedInPageLocators import MyAccountSignedInPageLocators


class MyAccountSignedInPage(MyAccountSignedInPageLocators):

    def __init__(self, driver):
        self.sl = SeleniumExtended(driver)

    def verify_user_is_signed_in(self):
        """
        Verifies user is signed in by checking the 'Log Out' button is visible
        on the left navigation bar.
        :return:
        """
        self.sl.wait_until_element_is_visible(self.LEFT_NAV_LOGOUT_BTN)
