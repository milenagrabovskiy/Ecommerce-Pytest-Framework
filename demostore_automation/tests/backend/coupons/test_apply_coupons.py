import pytest
import logging as logger

from demostore_automation.src.api_helpers.CouponAPIHelper import CouponAPIHelper
from demostore_automation.src.api_helpers.OrdersAPIHelper import OrdersAPIHelper
from demostore_automation.src.dao.coupons_dao import CouponsDAO
from demostore_automation.src.dao.customers_dao import CustomersDAO
from demostore_automation.src.dao.orders_dao import OrdersDAO
from demostore_automation.src.generic_helpers.generic_coupons_helper import GenericCouponsHelper
from demostore_automation.src.dao.products_dao import ProductsDAO
from demostore_automation.src.generic_helpers.generic_orders_helper import GenericOrdersHelper

@pytest.fixture(scope="module")
def apply_coupon_setup():
    pass

@pytest.mark.applycoupon
def test_apply_coupon_to_new_order():
    # fetch random product from DB
    product_dao = ProductsDAO()
    db_product = product_dao.get_random_product_from_db(qty=1)
    product_id = db_product[0]['ID']
    logger.info(f"DB product id: {product_id} DB product name: {db_product[0]['post_title']}")

    # fetch random customer from DB
    customers_dao = CustomersDAO()
    db_cust = customers_dao.get_random_customer_from_db(qty=1)
    customer_id = db_cust[0]['ID']
    logger.info(f"DB customer id: {customer_id}")

    # create order with custom args
    generic_orders_helper =GenericOrdersHelper()
    product_args = {"line_items": [{"product_id": product_id, "quantity": 1}]}
    product_args.update({"customer_id": customer_id})
    product_args.update({
        "shipping_lines": [
            {
                "method_id": "free_shipping",  # overwrite 'shipping_lines' for free shipping
                "method_title": "Free Shipping",
                "total": "0.00"
            }
        ]
    })
    order_response = generic_orders_helper.create_order(product_args)
    order_id = order_response['id']
    logger.info(f"Successfully created order with id: {order_id}")
    logger.info(f"Order total before coupon: {order_response['total']}")

    # get call for order confirming total is cart total and no coupons applied
    orders_api_helper = OrdersAPIHelper()
    get_order = orders_api_helper.call_retrieve_order(order_id)
    total_before = get_order['total']
    logger.info(f"GET order for order id: {order_id}: {get_order}")

    assert order_response['total'] == total_before, (f"Create order response total does not match GET order response total."
                                                           f"Create response: {order_response['total']}"
                                                           f"GET response: {get_order['total']}")


    # Fetch coupon from DB
    coupons_api_helper = CouponAPIHelper()
    coupons_dao = CouponsDAO()
    free_coupon = coupons_dao.fetch_coupon_by_text('ssqa100')
    assert free_coupon, "Coupon does not exist in DB"
    free_coupon_id = free_coupon[0]['ID']
    logger.info(f"Fetched free coupon from DB with id: {free_coupon_id}")

    # Get coupon details with GET call
    coupon_details = coupons_api_helper.call_retrieve_coupon(free_coupon_id)
    coupon_type = coupon_details['discount_type']
    coupon_expiration = coupon_details['date_expires']
    assert coupon_details['status'] == 'publish', f"Error. Coupon status: {coupon_details['status']}."
    generic_coupons_helper = GenericCouponsHelper()
    generic_coupons_helper.coupon_is_valid(free_coupon_id), "Coupon is expired"


    # make api PUT call for order and add coupon_lines
    coupon_code = "ssqa100"
    payload_update = {
        "coupon_lines": [{"code": coupon_code}]
    }
    update_response = orders_api_helper.call_update_order(order_id, payload_update)
    total_after = update_response['total']
    expected_total_after = '0.00'
    logger.info(f"PUT response with coupon: {update_response}")
    logger.info(f"Order total after applying coupon: {total_after}")

    assert total_before != total_after, "Coupon failed to be applied"
    assert update_response['discount_total'] == total_before, (f"Incorrect discount amount."
                                                               f"Actual: {update_response['discount_total']}."
                                                               f"Expected: {total_before}")
    assert total_after == expected_total_after, (f"Order total after coupon does not match expected."
                                                 f"Expected: {expected_total_after}, Actual: {total_after}")



