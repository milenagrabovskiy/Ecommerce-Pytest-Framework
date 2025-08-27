
import logging as logger
from datetime import datetime, timezone
from demostore_automation.src.api_helpers.CouponAPIHelper import CouponAPIHelper


class GenericCouponsHelper:

    def __init__(self):
        self.coupons_api_helper = CouponAPIHelper()

    def coupon_is_valid(self, coupon_id):
        get_coupon = self.coupons_api_helper.call_retrieve_coupon(coupon_id)
        expiration = get_coupon['date_expires']
        if not expiration:
           return True

        # convert to datetime object
        expiration_dt = datetime.fromisoformat(expiration).replace(tzinfo=timezone.utc)

        # compare with current UTC time
        return datetime.now(timezone.utc) < expiration_dt
