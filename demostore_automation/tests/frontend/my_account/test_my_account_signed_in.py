
import pytest
import time
from demostore_automation.src.pages.MyAccountSignedInPage import MyAccountSignedInPage
from demostore_automation.src.pages.MyAccountSignedOutPage import MyAccountSignedOutPage

pytestmark = [pytest.mark.feregression, pytest.mark.fesmoke, pytest.mark.my_account]



@pytest.mark.usefixtures("init_driver")
class TestMyAccountSignedIn:

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

        myacct = MyAccountSignedInPage(self.driver)

        myacct.get_side_navigation_menu()

    @pytest.mark.efe64
    def test_verify_account_details_match(self, create_registered_user):
        user_email = create_registered_user['email']
        myacct = MyAccountSignedInPage(self.driver)

        myacct.get_side_navigation_menu()
        myacct.go_to_account_details()

        email = myacct.get_my_acc_details_email()
        assert email == user_email, (f"ERROR. Email in account details does not match user email."
                                     f"Actual: {email}, Expected: {user_email}")
