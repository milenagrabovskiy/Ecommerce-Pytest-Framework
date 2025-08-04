
from selenium.webdriver.common.by import By


class CheckoutPageLocators:

    BILLING_FIRST_NAME_FIELD = (By.ID, 'billing-first_name')
    BILLING_LAST_NAME_FIELD = (By.ID, 'billing-last_name')
    BILLING_ADDRESS_1_FIELD = (By.ID, 'billing-address_1')
    BILLING_CITY_FIELD = (By.ID, 'billing-city')
    BILLING_ZIP_FIELD = (By.ID, 'billing-postcode')
    BILLING_PHONE_FIELD = (By.ID, 'billing-phone')
    BILLING_EMAIL_FIELD = (By.ID, 'email')
    BILLING_COUNTRY_DROPDOWN = (By.ID, 'billing-country')
    BILLING_STATE_DROPDOWN = (By.ID, 'billing-state')

    PLACE_ORDER_BTN = (By.XPATH, '//*[@id="post-8"]/div/div/div[4]/div[2]/form/div[5]')