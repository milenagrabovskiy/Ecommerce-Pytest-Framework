
import logging as logger
from datetime import datetime, timezone
from demostore_automation.src.api_helpers.CouponAPIHelper import CouponAPIHelper
from demostore_automation.src.api_helpers.OrdersAPIHelper import OrdersAPIHelper


class GenericCouponsHelper:

    def __init__(self):
        self.coupons_api_helper = CouponAPIHelper()
        self.orders_api_helper = OrdersAPIHelper()

    def coupon_is_valid(self, coupon_id):
        get_coupon = self.coupons_api_helper.call_retrieve_coupon(coupon_id)
        expiration = get_coupon['date_expires']
        if not expiration:
           return True

        # convert to datetime object
        expiration_dt = datetime.fromisoformat(expiration).replace(tzinfo=timezone.utc)

        # compare with current UTC time
        return datetime.now(timezone.utc) < expiration_dt

    def verify_coupon_successfully_applied(self, order_id, total_before, coupon_id, expected_discount):
        order_response = self.orders_api_helper.call_retrieve_order(order_id)
        coupon_response = self.coupons_api_helper.call_retrieve_coupon(coupon_id)
        discount_type = coupon_response['discount_type']

        total_before_float = float(total_before)
        expected_discount_float = float(expected_discount)

        if discount_type == 'percent':
            applied_discount = total_before_float * (float(expected_discount) / 100)

        else:
            applied_discount = min(expected_discount_float, total_before_float) # makes sure total is not negative! caps it at 0

        expected_discount_str = f"{applied_discount:.2f}"
        expected_total_after_str = f"{max(total_before_float - applied_discount, 0.0):.2f}" # max means total after is capped at 0

        total_after_str = order_response['total']  # API returns string
        discount_total_str = order_response['discount_total']  # API returns string

        assert total_before != float(
            total_after_str), f"Coupon failed to be applied. Total before coupon: {total_before} Total after coupon: {total_after_str}"
        assert discount_total_str == expected_discount_str, f"Incorrect discount amount. Actual: {discount_total_str}, Expected: {expected_discount_str}"
        assert total_after_str == expected_total_after_str, f"Order total after coupon does not match expected. Expected: {expected_total_after_str}, Actual: {total_after_str}"

        logger.info(f"Coupon applied successfully to order id: {order_id}")


    def verify_coupon_used_by_customer(self, coupon_id, customer_email, customer_id):
        coupon_response = self.coupons_api_helper.call_retrieve_coupon(coupon_id)
        coupon_users = [str(u).lower() for u in coupon_response['used_by']]  # normalize

        customer_id_str = str(customer_id)

        assert (customer_email in coupon_users) or (customer_id_str in coupon_users), \
            f"Customer with email: {customer_email} and id: {customer_id} not listed in 'used_by' field of coupon get api response. List of users: {coupon_users}"

        logger.info(
            f"Customer with email: {customer_email} or id: {customer_id} found in 'used_by' field of get coupon API response")


    def create_coupon_fixed_product(self, product_id):
        payload = {
            "code": "fixed_product_coupon",
            "discount_type": "fixed_product",
            "amount": "10.00",
            "individual_use": True,
            "exclude_sale_items": True,
            "minimum_amount": "0.00",
            "product_ids": [product_id]
        }
        return self.coupons_api_helper.call_create_coupon(payload, expected_status_code=201)