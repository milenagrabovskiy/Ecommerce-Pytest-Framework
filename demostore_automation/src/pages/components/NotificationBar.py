

from demostore_automation.src.selenium_extended.SeleniumExtended import SeleniumExtended
from demostore_automation.src.pages.locators.components.NotificationBarLocators import NotificationBarLocators




class NotificationBar(NotificationBarLocators):

    def __init__(self, driver):
        self.sl = SeleniumExtended(driver)

    def verify_notification_bar_is_displayed(self):
        self.sl.wait_until_element_is_visible(self.NOTIFICATION_BAR_TEXT)

    def verify_notification_bar_is_not_displayed(self):

        try:
            self.sl.wait_until_element_is_visible(self.NOTIFICATION_BAR_TEXT, timeout=3)
            raise Exception(f"The 'Notification Bar' should not be displayed but it is displayed.")
        except:
            print("Banner is not displayed.")

