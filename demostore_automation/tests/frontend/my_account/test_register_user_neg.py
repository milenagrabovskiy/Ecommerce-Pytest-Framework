

import pytest
from demostore_automation.src.pages.MyAccountSignedOutPage import MyAccountSignedOutPage
from demostore_automation.src.pages.MyAccountSignedInPage import MyAccountSignedInPage
from demostore_automation.src.utilities.genericUtilities import generate_random_string
from demostore_automation.src.utilities.genericUtilities import generate_random_email_and_password


pytestmark = [pytest.mark.feregression, pytest.mark.my_account, pytest.mark.my_acc_neg]

@pytest.mark.parametrize(
    "email,password,expected_error",
    [
        pytest.param(
            "abc@gmail",  # invalid email
            generate_random_email_and_password()["password"],  # valid random password
            "Please provide a valid email address."
        )
    ]
)

@pytest.mark.usefixtures("init_driver")
class TestRegisterUserNeg:


    @pytest.mark.tcid13
    @pytest.mark.pioneertcid2
    def test_register_user_invalid(self, email, password, expected_error):
        """
        Test to verify a valid user can register to the site.
        It generates a random email and password, then registers the user.
        :return:
        """
        # create objects
        myacct = MyAccountSignedInPage(self.driver)
        myacct_so = MyAccountSignedOutPage(self.driver)

        # go to my account page
        myacct_so.go_to_my_account()

        myacct_so.input_register_email(email)

        # fill in the password for registration
        myacct_so.input_register_password(password)

        # click on 'register'
        myacct_so.click_register_button()

        # verify error message
        myacct_so.wait_until_error_is_displayed(expected_error)

        # verify still on my account signed out page
        assert not myacct.is_user_signed_in()