
from demostore_automation.src.pages.locators.CheckoutPageLocators import CheckoutPageLocators

from demostore_automation.src.selenium_extended.SeleniumExtended import SeleniumExtended
from demostore_automation.src.utilities.genericUtilities import generate_random_email_and_password
from demostore_automation.src.configs.MainConfigs import MainConfigs

class CheckoutPage(CheckoutPageLocators):

    endpoint = '/checkout'

    def __init__(self, driver):
        self.driver = driver
        self.sl = SeleniumExtended(driver)

    def go_to_checkout_page(self):
        base_url = MainConfigs.get_base_url()
        checkout_url = base_url + self.endpoint
        self.driver.get(checkout_url)

    def input_billing_first_name(self, first_name=None):
        first_name = first_name if first_name else 'AutomationFname'
        self.sl.wait_and_input_text(self.BILLING_FIRST_NAME_FIELD, first_name)

    def input_billing_last_name(self, last_name=None):
        last_name = last_name if last_name else 'AutomationLname'
        self.sl.wait_and_input_text(self.BILLING_LAST_NAME_FIELD, last_name)

    def input_billing_street_address_1(self, address1=None):
        address1 = address1 if address1 else "123 Main st."
        self.sl.wait_and_input_text(self.BILLING_ADDRESS_1_FIELD, address1)

    def input_billing_city(self, city=None):
        city = 'San Francisco' if not city else city
        self.sl.wait_and_input_text(self.BILLING_CITY_FIELD, city)

    def input_billing_zip(self,  zip_code=None):
        zip_code = 94016 if not zip_code else zip_code
        self.sl.wait_and_input_text(self.BILLING_ZIP_FIELD, zip_code)

    def input_billing_phone_number(self, phone=None):
        phone = '4151111111' if not phone else phone
        self.sl.wait_and_input_text(self.BILLING_PHONE_FIELD, phone)

    def input_billing_email(self, email=None):
        if not email:
            rand_email = generate_random_email_and_password()
            email = rand_email['email']
        self.sl.wait_and_input_text(self.BILLING_EMAIL_FIELD, email)

    def select_billing_country(self, country=None):
        country = 'United States (US)' if not country else country
        self.sl.wait_and_select_dropdown(self.BILLING_COUNTRY_DROPDOWN, to_select=country, select_by="visible_text")

    def select_billing_state(self, state=None):
        state = 'California' if not state else state
        self.sl.wait_and_select_dropdown(self.BILLING_STATE_DROPDOWN, to_select=state, select_by="visible_text")

    def fill_in_billing_info(self, f_name=None, l_name=None, street1=None, city=None, zip_code=None, phone=None, email=None, state=None, country=None):
        self.input_billing_first_name(first_name=f_name)
        self.input_billing_last_name(last_name=l_name)
        self.input_billing_street_address_1(address1=street1)
        self.input_billing_city(city=city)
        self.input_billing_zip(zip_code=zip_code)
        self.input_billing_phone_number(phone=phone)
        self.input_billing_email(email=email)
        self.select_billing_country(country)
        self.select_billing_state(state=state)

    def click_place_order(self):
        self.sl.wait_and_click(self.PLACE_ORDER_BTN)