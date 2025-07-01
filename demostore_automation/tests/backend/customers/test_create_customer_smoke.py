
import logging as logger
import pytest
from demostore_automation.src.utilities.genericUtilities import generate_random_email_and_password
from demostore_automation.src.utilities.wooAPIUtility import WooAPIUtility
from demostore_automation.src.dao.customers_dao import CustomersDAO


pytestmark = [pytest.mark.beregression, pytest.mark.besmoke, pytest.mark.customers_api]


@pytest.mark.tcid29
@pytest.mark.pioneertcid11
def test_create_customer_only_email_password():

    # create payload with email and password only
    email_password = generate_random_email_and_password(email_prefix="pioneertcid11")
    email = email_password['email']
    password = email_password['password']

    print(email_password)
    # make the call
    woo_helper = WooAPIUtility()
    payload = {
        "email": email,
        "password": password
        }
    rs_body = woo_helper.post("customers", params=payload, expected_status_code=201)

    # verify response is good
    assert rs_body, f"Response of create customers call should not be empty."
    assert rs_body['id'], f"ID should be present in response."
    assert isinstance(rs_body['id'], int), f"The id in response of create customer should be numeric."
    assert email == rs_body['email'], f"Create customer endpoint email in response does not match in request." \
                                      f"Expected: {email}, Actual: {rs_body['email']}"
    assert rs_body['role'] == 'customer', f"Create new customer API, customer role should be 'customer' but " \
                                          f"it was '{rs_body['role']}'"

    # verify customer is created by checking the database
    customer_helper = CustomersDAO()
    db_info = customer_helper.get_customer_by_email(email)
    assert len(db_info) == 1, f"Expected 1 record for customer in 'users' table. But found: {len(db_info)}"
    assert db_info[0]['user_pass'], f"After creating user with api, the password field in DB is empty."

    expected_display_name = email.split('@')[0]

    assert db_info[0]['display_name'] == expected_display_name, f"Display name database does not match expected." \
                                                                f"Email: {email}, Expected display: {expected_display_name}" \
                                                                f"DB display name: {db_info[0]['display_name']}"
    assert db_info[0]['user_login'] == expected_display_name, f"user_login name database does not match expected." \
                                                                f"Email: {email}, Expected display: {expected_display_name}" \
                                                                f"DB display name: {db_info[0]['user_login']}"

@pytest.mark.tcid47
@pytest.mark.pioneertcid12
def test_create_customer_fail_for_existing_email():

    # get random existing customer (from api or from db) - in this example we get it from db
    cust_dao = CustomersDAO()
    rand_cust = cust_dao.get_random_customer_from_db()
    rand_email = rand_cust[0]['user_email']
    logger.debug(f"Random email for the test: {rand_email}")

    # call api to create customer with the existing user
    email_password = generate_random_email_and_password(email_prefix="pioneertcid11")
    random_password = email_password['password']
    woo_helper = WooAPIUtility()
    payload = {
        "email": rand_email,
        "password": random_password
        }
    rs_body = woo_helper.post("customers", params=payload, expected_status_code=400)

    # verify the api response is a failure
    assert rs_body['code'] == 'registration-error-email-exists', f"Create customer with existing user response does not" \
                                f"have expected text. Expected: 'registration-error-email-exists', Actual: {rs_body['code']}"

    assert rs_body['data']['status'] == 400, f"Unexpected status code in body of response. " \
                                             f"Expected 400 actual: {rs_body['data']['status']}"
    assert 'An account is already registered with your email address.' in rs_body['message'], f"Create customer with existing user " \
                            f"response body 'message' did not contain expected text."

@pytest.mark.tcid32
@pytest.mark.pioneertcid13
def test_create_customer_fail_when_no_password_is_provided():

    # get random email
    random_info = generate_random_email_and_password()

    payload = {"email": random_info["email"]}

    woo_api_utility = WooAPIUtility()
    rs_api = woo_api_utility.post(wc_endpoint="customers", params=payload, expected_status_code=400)

    assert rs_api['code'] == 'rest_missing_callback_param', f"The code field in response is not as expected. " \
                                                            f"Expected=rest_missing_callback_param' Actual= {rs_api['code']}"
    assert rs_api['message'] ==  'Missing parameter(s): password', f"bad message in response"

    assert rs_api['data']['params'] == ['password']
    assert rs_api['data']['status'] == 400



    # make create customer api call without including password in the payload
