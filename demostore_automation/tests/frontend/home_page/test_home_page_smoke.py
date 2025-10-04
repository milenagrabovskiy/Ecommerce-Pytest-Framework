"""Home Page Smoke Tests.

This module contains smoke tests for verifying the main functionality
and UI elements of the Home Page in the demo store application.

The tests focus on:
    * Product list visibility and count
    * Page heading correctness
    * Header menu visibility
    * Sorting dropdown presence and options
    * Product details visibility (names, images, prices)

These tests serve as a quick validation that the Home Page is working
as expected before running more extensive regression tests.
"""
import pytest
from selenium.webdriver.support.ui import Select
from demostore_automation.src.pages.HomePage import HomePage
from demostore_automation.src.pages.Header import Header


pytestmark = [pytest.mark.feregression, pytest.mark.fesmoke, pytest.mark.home_page]



@pytest.mark.usefixtures("init_driver")
class TestHomePageSmoke:
    """Smoke tests for the Home Page functionality of the demo store.

    This test suite covers the main UI elements and interactions on the
    homepage, including product listings, headings, header menu, sorting dropdown,
    and product details (names, images, and prices).
    """
    @pytest.fixture(scope='class')
    def setup(self, request):
        """Set up the homepage and header page objects for the test class.

        Args:
            request: Pytest request object for accessing the test class.
        """
        request.cls.homepage = HomePage(self.driver)
        request.cls.header = Header(self.driver)
        self.homepage.go_to_home_page()
        yield

    @pytest.mark.tcid1
    @pytest.mark.pioneertcid4
    def test_verify_number_of_products_displayed(self, setup):
        """Verify that the expected number of products are displayed on the homepage.

        Asserts:
            The number of product elements matches the expected count (14).
        """
        expected_number_of_products = 14

        displayed_products = self.homepage.get_all_product_elements()

        assert len(displayed_products) == expected_number_of_products, \
            f"Unexpected number of products displayed on home page. " \
            f"Expected: {expected_number_of_products}, Actual: {len(displayed_products)}"

    @pytest.mark.tcid67
    @pytest.mark.pioneertcid5
    def test_verify_heading_is_displayed(self, setup):
        """Verify that the main heading is correctly displayed on the homepage.

        Asserts:
            The displayed heading text matches the expected heading ('Shop').
        """
        expected_heading = 'Shop'
        displayed_heading = self.homepage.get_displayed_heading()
        assert displayed_heading == expected_heading, \
            f"Displayed heading in home page is not as expected. " \
            f"Expected: {expected_heading}, Actual: {displayed_heading}"

    @pytest.mark.pioneertcid6
    def test_verify_header_menu_is_displayed(self, setup):
        """Verify that all header menu items are visible on the homepage."""
        self.header.assert_all_menu_items_displayed()

    @pytest.mark.efe49
    def test_verify_sorting_menu_present(self, setup):
        """Verify that the product sorting dropdown is present and has multiple options.

        Uses the Selenium Select class to inspect the dropdown options.
        Asserts:
            Dropdown contains more than one option.
        """
        dropdown_menu = self.homepage.get_sorting_dropdown_menu()
        select = Select(dropdown_menu) #using select class because element is a select element (with select tag).
        options = select.options
        assert len(options) > 1, "Multiple options in dropdown sort-by menu not present in UI"

    @pytest.mark.efe50
    def test_verify_product_names_displayed(self, setup):
        """Verify that all product names are visible on the homepage.

        Asserts:
            Each product name element is displayed in the UI.
        """
        names = self.homepage.get_product_names()
        assert all(name.is_displayed() for name in names), "Product names are not displayed on home page"

    @pytest.mark.efe51
    def test_verify_product_images_displayed(self, setup):
        """Verify that all product images are visible on the homepage.

        Asserts:
            Each product image element is displayed in the UI.
        """
        images = self.homepage.get_product_images()
        assert all(image.is_displayed() for image in images), "Product images are not displayed on home page"
    @pytest.mark.efe52
    def test_verify_product_prices_displayed(self, setup):
        """Verify that all product prices are visible on the homepage.

        Asserts:
            Each product price element is displayed in the UI.
        """
        prices = self.homepage.get_product_prices()
        assert all(price.is_displayed() for price in prices), "Product prices are not displayed on home page"