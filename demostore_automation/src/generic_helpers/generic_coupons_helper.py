"""Helper module for managing and verifying coupons in orders.

Provides methods to retrieve, create, and validate coupons, apply them
to orders, and verify their usage by customers.
"""
import logging as logger
from datetime import datetime, timezone
from demostore_automation.src.api_helpers.CouponAPIHelper import CouponAPIHelper
from demostore_automation.src.api_helpers.OrdersAPIHelper import OrdersAPIHelper
from demostore_automation.src.dao.coupons_dao import CouponsDAO
from demostore_automation.src.utilities.genericUtilities import generate_random_string


class GenericCouponsHelper:
    """Generic helper class for creating, retrieving, and validating coupons.

    Provides functionality to:
      - Retrieve or create coupons based on discount type.
      - Verify if a coupon is valid or expired.
      - Verify that a coupon was successfully applied to an order.
      - Verify that a customer has used a coupon.
      - Create fixed product coupons with random codes.

    Attributes:
        coupons_api_helper (CouponAPIHelper): API helper for coupon endpoints.
        orders_api_helper (OrdersAPIHelper): API helper for order endpoints.
        coupons_dao (CouponsDAO): Data access object for coupons.

    Initialization:
        Sets up API helpers for coupons and orders and initializes
        the coupons DAO for database access.
    """
    def __init__(self):
        self.coupons_api_helper = CouponAPIHelper()
        self.orders_api_helper = OrdersAPIHelper()
        self.coupons_dao = CouponsDAO()

    def get_coupon(self, discount_type, get_order=None, coupon_ids=None):
        """Retrieve or create a coupon based on discount type.

        Args:
            discount_type (str): Type of discount ('percent', 'fixed_cart',
                                 'fixed_product', 'free_coupon').
            get_order (dict, optional): Order data for fixed product coupon creation.
            coupon_ids (list, optional): List to track created coupon IDs.

        Returns:
            tuple: (coupon_id, coupon_code)
        """
        if discount_type == "free_coupon":
            coupon = self.coupons_dao.fetch_coupon_by_text('ssqa100')
            coupon_id = coupon[0]['ID']
            coupon_code = coupon[0]['post_title']

        elif discount_type == 'fixed_product':
            product_id_in_order = get_order['line_items'][0]['product_id']
            coupon = self.create_coupon_fixed_product(product_id_in_order)
            coupon_id = coupon['id']
            coupon_code = coupon['code']
            if coupon_ids is not None:
                coupon_ids.append(coupon_id)

        else:
            coupon = self.coupons_dao.fetch_coupon_by_discount_type(discount_type)
            assert coupon, f"No coupons found in DB with discount type: {discount_type}"
            coupon_id = coupon[0]['ID']
            coupon_code = coupon[0]['post_title']
        return coupon_id, coupon_code

    def coupon_is_valid(self, coupon_id):
        """Check if a coupon is still valid (not expired).

        Args:
            coupon_id (int): ID of the coupon to check.

        Returns:
            bool: True if valid, False if expired.
        """
        get_coupon = self.coupons_api_helper.call_retrieve_coupon(coupon_id)
        expiration = get_coupon['date_expires']
        if not expiration:
           return True

        # convert to datetime object
        expiration_dt = datetime.fromisoformat(expiration).replace(tzinfo=timezone.utc)

        # compare with current UTC time
        return datetime.now(timezone.utc) < expiration_dt

    def verify_coupon_successfully_applied(self, order_id, total_before, coupon_id, expected_discount):
        """Verify that a coupon has been correctly applied to an order.

        Args:
            order_id (int): ID of the order.
            total_before (float): Order total before coupon application.
            coupon_id (int): ID of the applied coupon.
            expected_discount (float): Expected discount amount.

        Raises:
            AssertionError: If coupon was not applied correctly or totals mismatch.
        """
        order_response = self.orders_api_helper.call_retrieve_order(order_id)
        coupon_response = self.coupons_api_helper.call_retrieve_coupon(coupon_id)
        discount_type = coupon_response['discount_type']

        total_before_float = float(total_before)
        expected_discount_float = float(expected_discount)
        total_after_float = float(order_response['total'])
        discount_total_float = float(order_response['discount_total'])

        if discount_type == 'percent':
            applied_discount = total_before_float * (expected_discount_float / 100)
        else:
            applied_discount = min(expected_discount_float, total_before_float)

        applied_discount_rounded = round(applied_discount, 2)
        expected_total_after_float = round(max(total_before_float - applied_discount_rounded, 0.0), 2)

        assert round(total_before_float, 2) != round(total_after_float, 2), \
            f"Coupon failed to be applied. Total before coupon: {total_before} Total after coupon: {total_after_float}"
        assert round(discount_total_float, 2) == applied_discount_rounded, \
            f"Incorrect discount amount. Actual: {discount_total_float}, Expected: {applied_discount_rounded}"
        assert round(total_after_float, 2) == expected_total_after_float, \
            f"Order total after coupon does not match expected. Expected: {expected_total_after_float}, Actual: {total_after_float}"

        logger.info(f"Coupon applied successfully to order id: {order_id}")

    def verify_coupon_used_by_customer(self, coupon_id, customer_email, customer_id):
        """Verify that a customer is listed as having used a coupon.

        Args:
            coupon_id (int): Coupon ID to check.
            customer_email (str): Customer email.
            customer_id (int): Customer ID.

        Raises:
            AssertionError: If customer not listed in 'used_by' field of coupon.
        """
        coupon_response = self.coupons_api_helper.call_retrieve_coupon(coupon_id)
        coupon_users = [str(u).lower() for u in coupon_response['used_by']]  # normalize

        customer_id_str = str(customer_id)

        assert (customer_email in coupon_users) or (customer_id_str in coupon_users), \
            f"Customer with email: {customer_email} and id: {customer_id} not listed in 'used_by' field of coupon get api response. List of users: {coupon_users}"

        logger.info(
            f"Customer with email: {customer_email} or id: {customer_id} found in 'used_by' field of get coupon API response")


    def create_coupon_fixed_product(self, product_id):
        """Create a fixed-product coupon for a specific product.

        Args:
            product_id (int): Product ID for which the coupon applies.

        Returns:
            dict: API response of the created coupon.
        """
        payload = {
            "code": generate_random_string(),
            "discount_type": "fixed_product",
            "amount": "10.00",
            "individual_use": True,
            "exclude_sale_items": True,
            "minimum_amount": "0.00",
            "product_ids": [product_id]
        }
        return self.coupons_api_helper.call_create_coupon(payload, expected_status_code=201)


    def create_expired_coupon(self):
        """Create a coupon that is already expired.

        Returns:
            dict: API response for the expired coupon.
        """

        payload = {
            "code": generate_random_string(),
            "discount_type": "percent",
            "amount": "10",
            "date_expires": "2024-10-31T21:19:16"
        }
        return self.coupons_api_helper.call_create_coupon(payload, expected_status_code=201)


    def apply_coupon_to_order(self, coupon_code, order_id, expected_status_code=200):
        """Apply a coupon to an existing order via API.

        Args:
            coupon_code (str): Coupon code.
            order_id (int): Order ID.
            expected_status_code (int, optional): Expected API response code (default 200).

        Returns:
            dict: API response for the order update.
        """
        payload_update = {"coupon_lines": [{"code": coupon_code}]}
        return self.orders_api_helper.call_update_order(order_id, payload_update, expected_status_code=expected_status_code)