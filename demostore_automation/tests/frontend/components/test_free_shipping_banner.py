

import pytest

from demostore_automation.src.pages.HomePage import HomePage
from demostore_automation.src.pages.CartPage import CartPage
from demostore_automation.src.pages.components.NotificationBar import NotificationBar
from demostore_automation.src.pages.CheckoutPage import CheckoutPage
from demostore_automation.src.pages.MyAccountSignedOutPage import MyAccountSignedOutPage


@pytest.mark.notificationbar
@pytest.mark.feregression
@pytest.mark.usefixtures("init_driver")
class TestFreeShippingBanner:


    @pytest.mark.tcid69
    @pytest.mark.pioneertcid7
    def test_verify_free_shipping_banner_displayed_in_home_page(self):
        # go to home page
        # home_page = HomePage(self.driver)
        # home_page.go_to_home_page()
        HomePage(self.driver).go_to_home_page()

        # verify the notification bar is displayed
        NotificationBar(self.driver).verify_notification_bar_is_displayed()

    @pytest.mark.tcid70
    @pytest.mark.pioneertcid8
    def test_verify_free_shipping_banner_displayed_in_cart_page(self):
        # go to home page
        CartPage(self.driver).go_to_cart_page()

        # verify the notification bar is displayed
        NotificationBar(self.driver).verify_notification_bar_is_displayed()

    @pytest.mark.tcid71
    @pytest.mark.pioneertcid9
    def test_verify_free_shipping_banner_displayed_in_checkout_page(self):
        home_page = HomePage(self.driver)
        home_page.go_to_home_page()
        home_page.click_first_add_to_cart_button()
        CheckoutPage(self.driver).go_to_checkout_page()

        # verify the notification bar is displayed
        NotificationBar(self.driver).verify_notification_bar_is_displayed()

    @pytest.mark.tcid72
    @pytest.mark.pioneertcid10
    def test_verify_free_shipping_banner_not_displayed_in_my_account_page(self):
        MyAccountSignedOutPage(self.driver).go_to_my_account()
        # verify the notification bar is not displayed
        NotificationBar(self.driver).verify_notification_bar_is_not_displayed()