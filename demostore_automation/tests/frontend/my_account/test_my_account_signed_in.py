"""Tests for verifying the My Account page functionality for signed-in users.

This module validates that key elements of the My Account page are displayed correctly
and that user-specific information matches registered data. It ensures a consistent
user experience after login, including the visibility of headers, side navigation,
and account details.
"""

import pytest
from demostore_automation.src.pages.MyAccountSignedInPage import MyAccountSignedInPage
from demostore_automation.src.pages.MyAccountSignedOutPage import MyAccountSignedOutPage
from demostore_automation.src.utilities.genericUtilities import generate_random_string

pytestmark = [pytest.mark.feregression, pytest.mark.fesmoke, pytest.mark.my_account2]

@pytest.fixture(scope='class')
def setup(request, create_registered_user):
    request.cls.myacct = MyAccountSignedInPage(request.cls.driver)
    request.cls.myacct_so = MyAccountSignedOutPage(request.cls.driver)
    request.cls.email = create_registered_user['email']
    request.cls.password = create_registered_user['password']

@pytest.mark.usefixtures("init_driver")
class TestMyAccountSignedIn:
    """Test suite for verifying signed-in user interactions on the My Account page."""

    @pytest.mark.efe62
    def test_verify_my_acct_details_header(self, setup):
        """Verify that the My Account page heading is displayed correctly.

        This test ensures that when navigating to the My Account page,
        the correct header text ('My account') is shown, indicating
        that the user has successfully reached the My Account section.

        """
        expected_header = 'Account details'
        header = self.myacct.go_to_account_details()
        assert header == expected_header, f"ERROR. Wrong heading. Expected: {expected_header}, Actual: {header}"

    @pytest.mark.efe65
    def test_verify_my_acct_header(self, setup):
        """Verify that the My Account page heading is displayed correctly.

        This test ensures that when navigating to the My Account page,
        the correct header text ('My account') is shown, indicating
        that the user has successfully reached the My Account section.

        """
        self.myacct.go_to_dashboard()
        expected_header = 'My account'
        header = self.myacct.get_my_account_header()
        assert header == expected_header, f"ERROR. Wrong heading. Expected: {expected_header}, Actual: {header}"

    @pytest.mark.efe63
    def test_verify_side_navigation(self, create_registered_user, setup):
        """Verify the side navigation menu is visible for signed-in users.

        Ensures that after login, the side navigation panel is present, providing access
        to account-related sections like Orders, Downloads, and Account Details.

        Args:
            create_registered_user (dict): Fixture providing registered user credentials.
        """
        self.myacct.get_side_navigation_menu()

    @pytest.mark.efe64
    def test_verify_account_details_match(self, create_registered_user, setup):
        """Verify the account email matches the registered user email.

        Navigates to 'Account details' and retrieves the email displayed. Validates that
        it matches the registered user's email to ensure data consistency.

        Args:
            create_registered_user (dict): Fixture providing registered user credentials.

        Expected Result:
            Displayed email equals the registered user's email.
        """
        self.myacct.get_side_navigation_menu()
        self.myacct.go_to_account_details()

        email = self.myacct.get_my_acc_details_email()
        assert email == self.email, (f"ERROR. Email in account details does not match user email."
                                     f"Actual: {email}, Expected: {self.email}")

    @pytest.mark.efe66
    def test_change_password(self, create_registered_user, setup):
        """Verify that a signed-in user can successfully change their password.

        This test navigates to the Account Details page, updates first and last
        names, changes the account password, and validates that a success message
        appears. It also confirms that the user can log back in using the new password.

        Expected Result:
            The system displays a success message confirming the password change,
            and login with the new password is successful.
        """
        # go to account details
        self.myacct.get_side_navigation_menu()
        self.myacct.go_to_account_details()

        # input first and last name
        f_name = 'John'
        l_name = 'Doe'
        self.myacct.input_first_name(f_name)
        self.myacct.input_last_name(l_name)

        # input current password
        self.myacct.input_current_password(self.password)

        # create new password
        new_password = generate_random_string()

        # input new password twice
        self.myacct.input_new_password(new_password=new_password)
        self.myacct.confirm_new_password(new_password=new_password)

        # click save changes
        self.myacct.click_on_save_changes_btn()

        # verify success message that password was changed
        expected_message = 'Account details changed successfully.'
        message = self.myacct.get_password_changed_success_msg()
        assert message == expected_message, (f"ERROR. Wrong message displayed after changing password."
                                             f"Actual: {message}, Expected: {expected_message}")

        # logout
        self.myacct.click_logout()

        # login with new password
        self.myacct_so.input_login_username(self.email)
        self.myacct_so.input_login_password(new_password)
        self.myacct_so.click_login_button()

        # verify user is signed in
        self.myacct.verify_user_is_signed_in()