"""This module contains automated tests for the 'Privacy Policy' link on the My Account page
of the DemoStore website. Tests verify that navigation works and that the correct page
breadcrumbs are displayed.
"""
import pytest
from demostore_automation.conftest import init_driver
from demostore_automation.src.pages.MyAccountSignedOutPage import MyAccountSignedOutPage


pytestmark = [pytest.mark.feregression, pytest.mark.fesmoke, pytest.mark.my_account]

@pytest.mark.efe48
@pytest.mark.usefixtures("init_driver")
class TestPrivacyPolicy:
    """Test suite for verifying the 'Privacy Policy' link and page navigation.

    Attributes:
        driver: Selenium WebDriver instance provided by the init_driver fixture.
    """

    @pytest.mark.xfail
    @pytest.mark.efe1
    def test_privacy_policy_link(self):
        """
        Verify that the 'Privacy Policy' link on the My Account page navigates correctly.

        Steps:
        1. Go to the My Account page.
        2. Click on the 'Privacy Policy' link.
        3. Verify that the breadcrumbs contain the text 'Privacy Policy'.

        Notes:
            This test is marked as expected to fail (xfail) because the Privacy Policy
            link currently leads to a 404 page.
        """
        my_acc = MyAccountSignedOutPage(self.driver)

        # go to my account
        my_acc.go_to_my_account()

        # click on privacy policy link
        my_acc.click_on_privacy_link()

        breadcrumbs_text = my_acc.get_bread_crumbs_text()

        assert "Privacy Policy" in breadcrumbs_text, f"'Privacy Policy' not found in breadcrumbs: {breadcrumbs_text}"
        # xfailed because privacy policy link gives 404 page not found error