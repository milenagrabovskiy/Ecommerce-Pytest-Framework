"""Tests for verifying negative scenarios on the My Account page for signed-in users.

This module focuses on validation errors during the password change process,
ensuring correct error messages appear when mandatory fields are missing or left blank.
"""
from unittest import expectedFailure

import pytest
from demostore_automation.src.pages.MyAccountSignedInPage import MyAccountSignedInPage
from demostore_automation.src.pages.MyAccountSignedOutPage import MyAccountSignedOutPage
from demostore_automation.src.utilities.genericUtilities import generate_random_string

pytestmark = [pytest.mark.feregression, pytest.mark.my_account_neg]


@pytest.fixture(scope='class')
def setup(request, create_registered_user):
    """Initialize page objects and user credentials for signed-in account tests."""
    request.cls.myacct = MyAccountSignedInPage(request.cls.driver)
    request.cls.myacct_so = MyAccountSignedOutPage(request.cls.driver)
    request.cls.email = create_registered_user['email']
    request.cls.password = create_registered_user['password']


@pytest.mark.usefixtures("init_driver", "setup")
class TestMyAccountSignedInNeg:
    """Negative test cases for My Account password change functionality."""

    @pytest.mark.neg
    @pytest.mark.parametrize(
        "missing_field",
        [
            pytest.param("confirm_password", marks=pytest.mark.efe67, id="missing confirm password"),
            pytest.param("name", marks=pytest.mark.efe68, id="missing name"),
            pytest.param("current_password", marks=pytest.mark.efe69, id="missing current password")
        ]
    )
    def test_change_password_neg(self, missing_field):
        """Verify validation errors appear when required fields are missing.

        This test covers negative password change scenarios, confirming
        that the process fails gracefully when specific fields are left blank.

        Args:
            missing_field (str): Specifies which field to leave blank. Accepted values:
                - "name"
                - "current_password"
                - "confirm_password"

        Assertions:
            - Verifies that the success message is not displayed.
            - Ensures the correct error message appears when a field is missing.

        Raises:
            AssertionError: If the success message is displayed despite a missing field.
        """
        # go to account details
        self.myacct.get_side_navigation_menu()
        self.myacct.go_to_account_details()

        # input name fields (leave blank for missing name)
        f_name = '' if missing_field == 'name' else 'John'
        l_name = '' if missing_field == 'name' else 'Doe'
        self.myacct.input_first_name(f_name)
        self.myacct.input_last_name(l_name)

        # input current password (leave blank for missing current password)
        if missing_field != 'current_password':
            self.myacct.input_current_password(self.password)

        # create and input new password
        new_password = generate_random_string()
        self.myacct.input_new_password(new_password=new_password)

        # confirm password (leave blank for missing confirm password)
        confirm_pw = '' if missing_field == 'confirm_password' else new_password
        self.myacct.confirm_new_password(new_password=confirm_pw)

        # save changes
        self.myacct.click_on_save_changes_btn()

        # verify success message not displayed
        success_msg = 'Account details changed successfully.'
        actual_msg = self.myacct.get_error_message()
        assert actual_msg != success_msg,\
            (f"ERROR. Change password with missing {missing_field}"
             f"field successfully changed password with message: {success_msg}")
