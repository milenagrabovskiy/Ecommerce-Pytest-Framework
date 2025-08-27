
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

    def verify_coupon_successfully_applied(self, order_id, total_before, expected_total_after, coupon_id, expected_discount):
        order_response = self.orders_api_helper.call_retrieve_order(order_id)
        coupon_response = self.coupons_api_helper.call_retrieve_coupon(coupon_id)
        discount_type = coupon_response['discount_type']
        total_before_float = float(total_before)
        if discount_type == 'percent':
            expected_discount_fl = total_before_float * (float(expected_discount) / 100) # convert to float to perform calculation
            expected_discount = f"{expected_discount_fl:.2f}" # round to 2 dec places and converts back intro string for assertions below
        total_after = order_response['total']
        assert total_before != total_after, f"Coupon failed to be applied. Total before coupon: {total_before} Total after coupon: {total_after}"
        assert order_response['discount_total'] == expected_discount, (f"Incorrect discount amount."
                                                                   f"Actual: {order_response['discount_total']}."
                                                                   f"Expected: {expected_discount}")
        assert total_after == expected_total_after, (f"Order total after coupon does not match expected."
                                                     f"Expected: {expected_total_after}, Actual: {total_after}")

        logger.info(f"Coupon applied successfully to order id: {order_id}")


    def verify_coupon_used_by_customer(self, coupon_id, customer_email, customer_id):
        coupon_response = self.coupons_api_helper.call_retrieve_coupon(coupon_id)
        coupon_users = [str(u).lower() for u in coupon_response['used_by']]  # normalize

        customer_id_str = str(customer_id)

        assert (customer_email in coupon_users) or (customer_id_str in coupon_users), \
            f"Customer with email: {customer_email} and id: {customer_id} not listed in 'used_by' field of coupon get api response. List of users: {coupon_users}"

        logger.info(
            f"Customer with email: {customer_email} or id: {customer_id} found in 'used_by' field of get coupon API response")