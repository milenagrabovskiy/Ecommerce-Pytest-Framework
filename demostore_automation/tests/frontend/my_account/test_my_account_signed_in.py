"""Tests for verifying the My Account page functionality for signed-in users.

This module validates that key elements of the My Account page are displayed correctly
and that user-specific information matches registered data. It ensures a consistent
user experience after login, including the visibility of headers, side navigation,
and account details.
"""

import pytest
from demostore_automation.src.pages.MyAccountSignedInPage import MyAccountSignedInPage
from demostore_automation.src.pages.MyAccountSignedOutPage import MyAccountSignedOutPage

pytestmark = [pytest.mark.feregression, pytest.mark.fesmoke, pytest.mark.my_account]



@pytest.mark.usefixtures("init_driver")
class TestMyAccountSignedIn:
    """Test suite for verifying signed-in user interactions on the My Account page."""

    @pytest.mark.efe62
    def test_verify_my_acct_header(self):
        """Verify that the My Account page heading is displayed correctly.

        This test ensures that when navigating to the My Account page,
        the correct header text ('My account') is shown, indicating
        that the user has successfully reached the My Account section.

        """
        myacct = MyAccountSignedOutPage(self.driver)
        expected_header = 'My account'
        header = myacct.get_my_acct_header()
        assert header == expected_header, f"ERROR. Wrong heading. Expected: {expected_header}, Actual: {header}"

    @pytest.mark.efe63
    def test_verify_side_navigation(self, create_registered_user):
        """Verify the side navigation menu is visible for signed-in users.

        Ensures that after login, the side navigation panel is present, providing access
        to account-related sections like Orders, Downloads, and Account Details.

        Args:
            create_registered_user (dict): Fixture providing registered user credentials.
        """
        myacct = MyAccountSignedInPage(self.driver)

        myacct.get_side_navigation_menu()

    @pytest.mark.efe64
    def test_verify_account_details_match(self, create_registered_user):
        """Verify the account email matches the registered user email.

        Navigates to 'Account details' and retrieves the email displayed. Validates that
        it matches the registered user's email to ensure data consistency.

        Args:
            create_registered_user (dict): Fixture providing registered user credentials.

        Expected Result:
            Displayed email equals the registered user's email.
        """
        user_email = create_registered_user['email']
        myacct = MyAccountSignedInPage(self.driver)

        myacct.get_side_navigation_menu()
        myacct.go_to_account_details()

        email = myacct.get_my_acc_details_email()
        assert email == user_email, (f"ERROR. Email in account details does not match user email."
                                     f"Actual: {email}, Expected: {user_email}")
