"""Module providing WooAPIUtility, a wrapper around the WooCommerce REST API client.
It simplifies API interactions by managing authentication, request sending,
response validation, and logging.
"""
from demostore_automation.src.configs.MainConfigs import MainConfigs
from demostore_automation.src.utilities.credentialsUtility import CredentialsUtility
from woocommerce import API
import logging as logger

class WooAPIUtility:
    """Wrapper around WooCommerce REST API using the 'woocommerce' Python package.
    Initializes API client with credentials and base URL from configuration utilities.

    Attributes:
        wcapi (API): Instance of WooCommerce API client.
        base_url (str): Base URL for the WooCommerce API.
    """

    def __init__(self):

        wc_creds = CredentialsUtility.get_woo_api_keys()

        self.base_url = MainConfigs.get_base_url()

        self.wcapi = API(
            url=self.base_url,
            consumer_key=wc_creds['woo_key'],
            consumer_secret=wc_creds['woo_secret'],
            version="wc/v3"
        )

    def assert_status_code(self):
        """Asserts that the actual response status code matches the expected status code.

        Raises:
            AssertionError: If actual status code does not equal expected status code.
        """
        assert self.status_code == self.expected_status_code, f"Bad Status code." \
          f"Expected {self.expected_status_code}, Actual status code: {self.status_code}," \
          f"URL: {self.url}, Response Json: {self.rs_json}"

    def post(self, wc_endpoint, params=None, expected_status_code=200):
        """Send a POST request to a WooCommerce API endpoint.

        Args:
            wc_endpoint (str): The WooCommerce API endpoint to post to.
            params (dict, optional): Payload parameters to send with the POST request.
            expected_status_code (int, optional): Expected HTTP status code, defaults to 200.

        Returns:
            dict: JSON response from the API.

        Raises:
            AssertionError: If the response status code does not match expected_status_code.
        """

        rs_api = self.wcapi.post(wc_endpoint, data=params)

        self.status_code = rs_api.status_code
        self.expected_status_code = expected_status_code
        self.rs_json = rs_api.json()
        self.endpoint = wc_endpoint
        self.url = rs_api.url
        self.assert_status_code()

        logger.debug(f"POST API response: {self.rs_json}")

        return self.rs_json

    def get(self, woo_endpoint, params=None, return_headers=False, expected_status_code=200):
        """Send a GET request to a WooCommerce API endpoint.

        Args:
            woo_endpoint (str): The WooCommerce API endpoint to get.
            params (dict, optional): Query parameters to send with the GET request.
            return_headers (bool, optional): Whether to return response headers alongside JSON. Defaults to False.
            expected_status_code (int, optional): Expected HTTP status code, defaults to 200.

        Returns:
            dict or dict: JSON response from the API, or dict containing 'response_json' and 'headers' if return_headers is True.

        Raises:
            AssertionError: If the response status code does not match expected_status_code.
        """

        rs_api = self.wcapi.get(woo_endpoint, params=params)
        self.status_code = rs_api.status_code
        self.expected_status_code = expected_status_code
        self.rs_json = rs_api.json()
        self.endpoint = woo_endpoint
        self.url = rs_api.url
        self.assert_status_code()

        logger.debug(f"GET API response: {self.rs_json}")
        if return_headers:
            return {'response_json': self.rs_json, 'headers': rs_api.headers}
        else:
            return self.rs_json

    def put(self, wc_endpoint, params=None, expected_status_code=200):
        """Send a PUT request to a WooCommerce API endpoint.

        Args:
            wc_endpoint (str): The WooCommerce API endpoint to put.
            params (dict, optional): Payload parameters to send with the PUT request.
            expected_status_code (int, optional): Expected HTTP status code, defaults to 200.

        Returns:
            dict: JSON response from the API.

        Raises:
            AssertionError: If the response status code does not match expected_status_code.
        """

        rs_api = self.wcapi.put(wc_endpoint, data=params)
        self.status_code = rs_api.status_code
        self.expected_status_code = expected_status_code
        self.rs_json = rs_api.json()
        self.endpoint = wc_endpoint
        self.url = rs_api.url
        self.assert_status_code()

        logger.debug(f"PUT API response: {self.rs_json}")

        return self.rs_json

    def delete(self, wc_endpoint, params=None, expected_status_code=200):
        """Send a DELETE request to a WooCommerce API endpoint.

        Args:
            wc_endpoint (str): The WooCommerce API endpoint to delete.
            params (dict, optional): Parameters to send with the DELETE request.
            expected_status_code (int, optional): Expected HTTP status code, defaults to 200.

        Returns:
            dict: JSON response from the API.

        Raises:
            AssertionError: If the response status code does not match expected_status_code.
        """

        rs_api = self.wcapi.delete(wc_endpoint, params=params)
        self.status_code = rs_api.status_code
        self.expected_status_code = expected_status_code
        self.rs_json = rs_api.json()
        self.endpoint = wc_endpoint
        self.url = rs_api.url
        self.assert_status_code()

        logger.debug(f"DELETE API response: {self.rs_json}")

        return self.rs_json


