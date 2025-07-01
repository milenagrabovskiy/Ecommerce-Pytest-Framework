
import pytest
from demostore_automation.src.pages.MyAccountSignedOutPage import MyAccountSignedOutPage

pytestmark = [pytest.mark.feregression, pytest.mark.fesmoke, pytest.mark.my_account]


@pytest.mark.usefixtures("init_driver")
class TestLoginNegative:


    @pytest.mark.tcid12
    @pytest.mark.pioneertcid1
    def test_login_none_existing_user(self):
        print("Testing None Existing User Login")

        my_acct_page = MyAccountSignedOutPage(self.driver)
        my_acct_page.go_to_my_account()
        my_acct_page.input_login_username("abcdef@supersqa.com")
        my_acct_page.input_login_password("abcdefg")
        my_acct_page.click_login_button()

        expected_err = "Unknown email address. Check again or try your username."
        my_acct_page.wait_until_error_is_displayed(expected_err)

        # breakpoint()



