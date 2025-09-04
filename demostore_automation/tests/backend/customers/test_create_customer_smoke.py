
import logging as logger
import pytest
from demostore_automation.src.utilities.genericUtilities import generate_random_email_and_password
from demostore_automation.src.utilities.wooAPIUtility import WooAPIUtility
from demostore_automation.src.dao.customers_dao import CustomersDAO


pytestmark = [pytest.mark.beregression, pytest.mark.besmoke, pytest.mark.customers_api]

class TestCreateCustomer:
    """Test suite for validating WooCommerce customer creation API endpoints."""
    def setup_method(self):
        """Set up the test before each test method is run.

        Initializes:
            - WooAPIUtility for API calls
            - CustomersDAO for DB access
            - Random test credentials (email and password)
            - A random existing customer from the database
        """
        self.woo_helper = WooAPIUtility()
        self.customer_dao = CustomersDAO()
        self.random_email = generate_random_email_and_password(email_prefix="test_user")["email"]
        self.random_password = generate_random_email_and_password()["password"]
        self.rand_cust = self.customer_dao.get_random_customer_from_db()
        self.existing_email = self.rand_cust[0]['user_email']
        self.api_customer_id = None

    def teardown_method(self):
        """Tear down test fixtures after each test method.

        Deletes the test customer that was created via the API if any.

        Raises:
            Exception: If deletion via API fails.
        """
        try:
            deleted_customer_count = 0
            if self.api_customer_id:
                self.woo_helper.delete(f"customers/{self.api_customer_id}", params={"force": True})
                logger.info(f"Deleted customer: {self.api_customer_id}")
                deleted_customer_count += 1
                logger.info(f"Deleted {deleted_customer_count} customers")

        except Exception as e:
            logger.warning(f"Error: {e}. Failed to delete customer with id: {self.api_customer_id}")

    @pytest.mark.ebe5
    @pytest.mark.tcid29
    @pytest.mark.pioneertcid11
    @pytest.mark.smoke
    def test_create_customer_only_email_password(self):
        """Test customer creation using only email and password.

        Verifies:
            - HTTP 201 response from API
            - Valid response fields such as ID and role
            - Customer is stored correctly in the database

        Raises:
            AssertionError: If any of the API or DB validations fail.
        """
        # make the call
        payload = {
            "email": self.random_email,
            "password": self.random_password
            }
        rs_body = self.woo_helper.post("customers", params=payload, expected_status_code=201)
        self.api_customer_id = rs_body['id']

        # verify response is good
        assert rs_body, f"Response of create customers call should not be empty."
        assert self.api_customer_id, f"ID should be present in response."
        assert isinstance(rs_body['id'], int), f"The id in response of create customer should be numeric."
        assert self.random_email == rs_body['email'], f"Create customer endpoint email in response does not match in request." \
                                          f"Expected: {self.random_email}, Actual: {rs_body['email']}"
        assert rs_body['role'] == 'customer', f"Create new customer API, customer role should be 'customer' but " \
                                              f"it was '{rs_body['role']}'"

        # verify customer is created by checking the database
        db_info = self.customer_dao.get_customer_by_email(self.random_email)
        assert len(db_info) == 1, f"Expected 1 record for customer in 'users' table. But found: {len(db_info)}"
        assert db_info[0]['user_pass'], f"After creating user with api, the password field in DB is empty."

        expected_display_name = self.random_email.split('@')[0]

        assert db_info[0]['display_name'] == expected_display_name, f"Display name database does not match expected." \
                                                                    f"Email: {self.random_email}, Expected display: {expected_display_name}" \
                                                                    f"DB display name: {db_info[0]['display_name']}"
        assert db_info[0]['user_login'] == expected_display_name, f"user_login name database does not match expected." \
                                                                    f"Email: {self.random_email}, Expected display: {expected_display_name}" \
                                                                    f"DB display name: {db_info[0]['user_login']}"
    @pytest.mark.ebe6
    @pytest.mark.tcid47
    @pytest.mark.pioneertcid12
    def test_create_customer_fail_for_existing_email(self):
        """Test API fails when trying to create a customer with an existing email.

        Verifies:
            - API returns 400
            - Appropriate error code and message are returned

        Raises:
            AssertionError: If API response doesn't contain expected error code/message.
        """

        # get random existing customer (from api or from db) - in this example we get it from db
        logger.debug(f"Fetched existing customer email: {self.existing_email}")

        # call api to create customer with the existing user
        payload = {
            "email": self.existing_email,
            "password": self.random_password
            }
        rs_body = self.woo_helper.post("customers", params=payload, expected_status_code=400)

        # verify the api response is a failure
        assert rs_body['code'] == 'registration-error-email-exists', f"Create customer with existing user response does not" \
                                    f"have expected text. Expected: 'registration-error-email-exists', Actual: {rs_body['code']}"

        assert rs_body['data']['status'] == 400, f"Unexpected status code in body of response. " \
                                                 f"Expected 400 actual: {rs_body['data']['status']}"
        assert 'An account is already registered with your email address.' in rs_body['message'], f"Create customer with existing user " \
                                f"response body 'message' did not contain expected text."

    @pytest.mark.ebe7
    @pytest.mark.tcid32
    @pytest.mark.pioneertcid13
    def test_create_customer_fail_when_no_password_is_provided(self):
        """Test API fails when no password is provided.

        Verifies:
            - API returns 400
            - Error message specifies missing password

        Raises:
            AssertionError: If missing param error is not correctly returned.
        """
        # password not included in payload for negative test
        payload = {"email": self.random_email}

        rs_api = self.woo_helper.post(wc_endpoint="customers", params=payload, expected_status_code=400)

        assert rs_api['code'] == 'rest_missing_callback_param', f"The code field in response is not as expected. " \
                                                                f"Expected=rest_missing_callback_param' Actual= {rs_api['code']}"
        assert rs_api['message'] ==  'Missing parameter(s): password', f"bad message in response"

        assert rs_api['data']['params'] == ['password']

        assert rs_api['data']['status'] == 400




