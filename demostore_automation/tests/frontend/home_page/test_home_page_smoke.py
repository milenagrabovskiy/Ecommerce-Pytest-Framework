
import pytest
from demostore_automation.src.pages.HomePage import HomePage
from demostore_automation.src.pages.Header import Header


pytestmark = [pytest.mark.feregression, pytest.mark.fesmoke, pytest.mark.home_page]



@pytest.mark.usefixtures("init_driver")
class TestHomePageSmoke:

    @pytest.fixture(scope='class')
    def setup(self, request):
        request.cls.homepage = HomePage(self.driver)
        request.cls.header = Header(self.driver)
        self.homepage.go_to_home_page()
        yield

    @pytest.mark.tcid1
    @pytest.mark.pioneertcid4
    def test_verify_number_of_products_displayed(self, setup):
        expected_number_of_products = 16

        displayed_products = self.homepage.get_all_product_elements()

        assert len(displayed_products) == expected_number_of_products, \
            f"Unexpected number of products displayed on home page. " \
            f"Expected: {expected_number_of_products}, Actual: {len(displayed_products)}"

    @pytest.mark.tcid67
    @pytest.mark.pioneertcid5
    def test_verify_heading_is_displayed(self, setup):
        expected_heading = 'Shop'
        displayed_heading = self.homepage.get_displayed_heading()
        assert displayed_heading == expected_heading, \
            f"Displayed heading in home page is not as expected. " \
            f"Expected: {expected_heading}, Actual: {displayed_heading}"

    @pytest.mark.pioneertcid6
    def test_verify_header_menu_is_displayed(self, setup):
        self.header.assert_all_menu_items_displayed()

