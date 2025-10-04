

import pytest
from demostore_automation.src.pages.MyAccountSignedOutPage import MyAccountSignedOutPage
from demostore_automation.src.pages.MyAccountSignedInPage import MyAccountSignedInPage
# from demostore_automation.src.utilities import genericUtilities
from demostore_automation.src.utilities.genericUtilities import generate_random_email_and_password


pytestmark = [pytest.mark.feregression, pytest.mark.fesmoke, pytest.mark.my_account]



@pytest.mark.usefixtures("init_driver")
class TestRegisterNewUserSmoke:


    @pytest.mark.tcid13
    @pytest.mark.pioneertcid2
    def test_register_valid_new_user(self):
        """
        Test to verify a valid user can register to the site.
        It generates a random email and password, then registers the user.
        :return:
        """
        # create objects
        myacct = MyAccountSignedOutPage(self.driver)
        myacct_sin = MyAccountSignedInPage(self.driver)

        # go to my account page
        myacct.go_to_my_account()

        random_info = generate_random_email_and_password()
        # fill in the username for registration
        myacct.input_register_email(random_info['email'])

        # fill in the password for registration
        myacct.input_register_password(random_info['password'])

        # click on 'register'
        myacct.click_register_button()

        # verify user is registered
        myacct_sin.verify_user_is_signed_in()

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