"""Helper module for WooCommerce coupon-related API interactions.

Contains the CouponAPIHelper class which wraps CRUD operations for coupons
using the WooAPIUtility class.

Provides methods to create, retrieve, and delete coupons via the WooCommerce REST API.
"""
from demostore_automation.src.utilities.wooAPIUtility import WooAPIUtility

class CouponAPIHelper:
    """Helper class to interact with WooCommerce coupons via API.

    Initializes a WooAPIUtility instance to perform API calls related to coupons.
    """

    def __init__(self):
        self.woo_helper = WooAPIUtility()

    def call_create_coupon(self, payload, expected_status_code=201):
        """Creates a new coupon using the WooCommerce API.

        Args:
            payload (dict): The coupon data to send in the API request.
            expected_status_code (int, optional): The expected HTTP status code for a successful creation. Defaults to 201.

        Returns:
            dict: The JSON response from the API representing the created coupon.
        """
        return self.woo_helper.post('coupons', params=payload, expected_status_code=expected_status_code)

    def call_retrieve_coupon(self, coupon_id):
        """Retrieves coupon details by coupon ID.

        Args:
            coupon_id (int or str): The ID of the coupon to retrieve.

        Returns:
            dict: The JSON response from the API representing the retrieved coupon.
        """
        return self.woo_helper.get(f'coupons/{coupon_id}', expected_status_code=200)

    def call_delete_coupon(self, coupon_id):
        """Deletes a coupon by coupon ID.

        Args:
            coupon_id (int or str): The ID of the coupon to delete.

        Returns:
            dict: The JSON response from the API after deleting the coupon.
        """
        return self.woo_helper.delete(f'coupons/{coupon_id}', expected_status_code=200)
