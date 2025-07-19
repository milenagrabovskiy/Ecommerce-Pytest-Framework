
from demostore_automation.src.utilities.wooAPIUtility import WooAPIUtility

class CouponAPIHelper:

    def __init__(self):
        self.woo_helper = WooAPIUtility()

    def call_create_coupon(self, payload, expected_status_code=201):
        return self.woo_helper.post('coupons', params=payload, expected_status_code=expected_status_code)

    def call_retrieve_coupon(self, coupon_id):
        return self.woo_helper.get(f'coupons/{coupon_id}', expected_status_code=200)

    def call_delete_coupon(self, coupon_id):
        return self.woo_helper.delete(f'coupons/{coupon_id}', expected_status_code=200)
