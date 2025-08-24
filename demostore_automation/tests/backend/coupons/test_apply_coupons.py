import pytest
import logging as logger

from demostore_automation.src.api_helpers.CouponAPIHelper import CouponAPIHelper
from demostore_automation.src.api_helpers.OrdersAPIHelper import OrdersAPIHelper
from demostore_automation.src.dao.coupons_dao import CouponsDAO
from demostore_automation.src.dao.orders_dao import OrdersDAO

@pytest.mark.applycoupon
def test_apply_coupon_to_existing_order():
#find or create order
    orders_dao = OrdersDAO()
    random_db_order = orders_dao.get_random_order_by_status("processing", qty=1)
    order_id = random_db_order[0]['order_id']
    logger.info(f"Order from DB: {random_db_order} Order ID: {order_id}")
# get call for order confirming total is cart total and no coupons applied
    orders_api_helper = OrdersAPIHelper()
    api_order = orders_api_helper.call_retrieve_order(order_id)
    total = api_order['total']
    logger.info(f"GET call for order id: {order_id}: {api_order}")
    logger.info(f"Order total before coupon: {total}")

# hardcode correct coupon code or randomly generated coupon code for neg tests
    coupons_api_helper = CouponAPIHelper()
    coupons_dao = CouponsDAO()
    free_coupon = coupons_dao.fetch_coupon_by_partial_string('ssqa100')
    logger.info(f"Fetched free coupon from DB with id: {free_coupon['coupon_id']}")
# verify total price is now 0 with ssqa100
