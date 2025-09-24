"""Negative tests for the My Account registration page.

This module contains tests for invalid registration inputs, including invalid emails,
weak passwords, and empty fields. It verifies that errors are displayed and users
cannot sign in with invalid credentials.
"""
import pytest
from demostore_automation.src.pages.MyAccountSignedOutPage import MyAccountSignedOutPage
from demostore_automation.src.pages.MyAccountSignedInPage import MyAccountSignedInPage
from demostore_automation.src.utilities.genericUtilities import generate_random_email_and_password


pytestmark = [pytest.mark.feregression, pytest.mark.my_account, pytest.mark.my_acc_neg]

@pytest.mark.parametrize(
    "email, password, expected_error",
    [
        pytest.param(
            "abc@gmail",  # invalid email
            generate_random_email_and_password()["password"],  # valid random password
            "Please provide a valid email address.",
            marks=pytest.mark.efe30, id='invalid email'
        ),
        pytest.param(
            generate_random_email_and_password()["email"],  # valid email
            "123",  # invalid password
            None,  # no error message expected; button is grayed out
            marks=pytest.mark.efe31, id='invalid password'
        ),
        pytest.param(
            'abc', 'abc', None,
            marks=pytest.mark.efe32, id='invalid email password'
        ),
        pytest.param(
            '', '', None,
            marks=pytest.mark.efe33, id='empty email and password'
        )
    ]
)

@pytest.mark.usefixtures("init_driver")
class TestRegisterUserNeg:
    """Tests for invalid user registration on the My Account page."""

    def test_register_user_invalid(self, email, password, expected_error):
        """Verify invalid registration prevents sign-in and displays errors.

        Args:
            email (str): The email address to use for registration.
            password (str): The password to use for registration.
            expected_error (str or None): Expected error message, or None if no error.

        Raises:
            AssertionError: If registration behavior does not match expected results.
        """
        # create objects
        myacct = MyAccountSignedInPage(self.driver)
        myacct_so = MyAccountSignedOutPage(self.driver)

        # go to my account page
        myacct_so.go_to_my_account()

        myacct_so.input_register_email(email)

        # fill in the password for registration
        myacct_so.input_register_password(password)

        # check if register button is enabled and click register btn
        if expected_error:
            assert myacct_so.is_register_btn_enabled(), "Register btn should be enabled"
            myacct_so.click_register_button()
            myacct_so.wait_until_error_is_displayed(expected_error) # verify error message

        # verify still on my account signed out page
        assert not myacct.is_user_signed_in(), "Error. User should not be signed in after invalid registration"