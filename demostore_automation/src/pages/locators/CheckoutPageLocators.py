
from selenium.webdriver.common.by import By


class CheckoutPageLocators:

    BILLING_FIRST_NAME_FIELD = (By.ID, 'billing_first_name')
    BILLING_LAST_NAME_FIELD = (By.ID, 'billing_last_name')
    BILLING_ADDRESS_1_FIELD = (By.ID, 'billing_address_1')
    BILLING_CITY_FIELD = (By.ID, 'billing_city')
    BILLING_ZIP_FIELD = (By.ID, 'billing_postcode')
    BILLING_PHONE_FIELD = (By.ID, 'billing_phone')
    BILLING_EMAIL_FIELD = (By.ID, 'billing_email')
    BILLING_COUNTRY_DROPDOWN = (By.ID, 'billing_country')
    BILLING_STATE_DROPDOWN = (By.ID, 'billing_state')

    PLACE_ORDER_BTN = (By.ID, 'place_order')