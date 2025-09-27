"""Tests for the 'Forgot Password' functionality on the My Account page.
    Covers both invalid and registered email scenarios.

Fixtures:
    init_driver : Sets up the WebDriver.
    go_to_my_acct : Navigates to My Account page before tests.
"""
import pytest

from demostore_automation.conftest import init_driver
from demostore_automation.src.pages.MyAccountSignedInPage import MyAccountSignedInPage
from demostore_automation.src.pages.MyAccountSignedOutPage import MyAccountSignedOutPage
from demostore_automation.src.utilities.genericUtilities import generate_random_email_and_password

pytestmark = [pytest.mark.feregression, pytest.mark.fesmoke, pytest.mark.my_account123]


@pytest.mark.usefixtures("init_driver")
class TestForgotPassword:
    """Tests the 'Lost your password?' flow.

    - Invalid email shows an error alert.
    - Registered email triggers password reset confirmation.

    Attributes:
        my_acct_page (MyAccountSignedOutPage): Page object for signed-out account page.
    """

    @pytest.fixture(scope='class')
    def go_to_my_acct(self, request):
        request.cls.my_acct_page = MyAccountSignedOutPage(self.driver)
        request.cls.my_acct_page.go_to_my_account()

    @pytest.mark.ty
    def test_lost_password_link_invalid_email(self, go_to_my_acct):
        """Verify 'Lost your password?' link for invalid email.

        Steps:
            1. Click the lost password link.
            2. Input a random invalid email.
            3. Verify the error alert is displayed.
        """
        # set email for registered user and invalid user
        email = generate_random_email_and_password()['email']

        # click on 'lost password' link and verify reset password page loaded
        self.my_acct_page.click_on_lost_password_link()
        self.my_acct_page.verify_on_password_reset_page()

        # input email to reset password
        self.my_acct_page.input_email_to_reset_password(email)

        self.my_acct_page.verify_wrong_email_alert_displayed() # invalid user gets alert

    @pytest.mark.qwe
    def test_lost_password_link_registered_email(self, create_registered_user, go_to_my_acct):
        """Verify 'Lost your password?' link for registered email.

        Steps:
            1. Log out of registered user session.
            2. Click the lost password link.
            3. Input the registered email.
            4. Verify password reset confirmation is displayed.
        """
        my_acct_si = MyAccountSignedInPage(self.driver)

        # fixture creates a registered user, then verifies user on my acc signed in page
        # must log out to see 'lost password' link
        my_acct_si.click_logout()

        # click on 'lost password' link and verify reset password page loaded
        self.my_acct_page.click_on_lost_password_link()
        self.my_acct_page.verify_on_password_reset_page()

        # input email to reset password
        email = create_registered_user['email']
        self.my_acct_page.input_email_to_reset_password(email)

        self.my_acct_page.verify_password_reset_sent()  # registered user gets confirmation