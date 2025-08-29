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
    products_dao = ProductsDAO()
    customers_dao = CustomersDAO()
    coupons_dao = CouponsDAO()
    random_product = products_dao.get_random_product_from_db(qty=1)[0]
    random_customer = customers_dao.get_random_customer_from_db(qty=1)[0]

    info = {
        "product_id": random_product['ID'],
        "customer_id": random_customer['ID'],
        "customer_email": random_customer['user_email'].lower(),
        "orders_api_helper": OrdersAPIHelper(),
        "coupons_api_helper": CouponAPIHelper(),
        "generic_orders_helper": GenericOrdersHelper(),
        "generic_coupons_helper": GenericCouponsHelper(),
        "random_product": random_product,
        "random_customer": random_customer,
        "coupons_dao": coupons_dao,
        "order_ids": [],
        "coupon_ids": []
    }
    yield info

    for ord_id in info["order_ids"]: # teardown
        info["orders_api_helper"].call_delete_order(ord_id)
        logger.info(f"Successfully deleted order id: {ord_id}")

    for coupon_id in info["coupon_ids"]:
        info["coupons_api_helper"].call_delete_coupon(coupon_id)
        logger.info(f"Successfully deleted coupon id: {coupon_id}")


@pytest.mark.parametrize(
    "discount_type",
    [
        pytest.param("percent", marks=[pytest.mark.applycoupon1]),
        pytest.param("fixed_cart", marks=[pytest.mark.applycoupon2]),
        pytest.param("fixed_product", marks=[pytest.mark.applycoupon3]),
        pytest.param("free_coupon", marks=[pytest.mark.applycoupon4])
    ]
)

@pytest.mark.applycoupon
def test_apply_coupon_to_new_order(apply_coupon_setup, discount_type):
    if discount_type == "fixed_product":
        product_id = 34 # hardcoded for V-neck shirt, a reg price variable product
    # fetch random product from DB
    else:
        product_id = apply_coupon_setup['product_id']
    logger.info(f"DB product id: {product_id} DB product name: {apply_coupon_setup['random_product']['post_title']}")

    # fetch random customer from DB
    customer_id = apply_coupon_setup['customer_id']
    customer_email = apply_coupon_setup['customer_email']
    logger.info(f"DB customer id: {customer_id} DB customer email: {customer_email}")

    # create order with custom args
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
    order_response = apply_coupon_setup['generic_orders_helper'].create_order(product_args)
    order_id = order_response['id']
    apply_coupon_setup['order_ids'].append(order_id) # for teardown
    logger.info(f"Successfully created order with id: {order_id}")
    logger.info(f"Order total before coupon: {order_response['total']}")

    # get call for order confirming total is cart total and no coupons applied
    get_order = apply_coupon_setup['orders_api_helper'].call_retrieve_order(order_id)
    total_before = get_order['total']
    logger.info(f"GET order for order id: {order_id}: {get_order}")

    assert order_response['total'] == total_before, (f"Create order response total does not match GET order response total."
                                                           f"Create response: {order_response['total']}"
                                                           f"GET response: {get_order['total']}")

    # Fetch coupon from DB or create coupon for 'fixed_product'
    if discount_type == "free_coupon":
        coupon = apply_coupon_setup['coupons_dao'].fetch_coupon_by_text('ssqa100')
        coupon_id = coupon[0]['ID']
        coupon_code = coupon[0]['post_title']

    elif discount_type == 'fixed_product':
        product_id_in_order = get_order['line_items'][0]['product_id']
        coupon = apply_coupon_setup['generic_coupons_helper'].create_coupon_fixed_product(product_id_in_order)
        coupon_id = coupon['id']
        coupon_code = coupon['code']
        apply_coupon_setup["coupon_ids"].append(coupon_id)

    else:
        coupon = apply_coupon_setup['coupons_dao'].fetch_coupon_by_discount_type(discount_type)
        assert coupon, f"No coupons found in DB with discount type: {discount_type}"
        coupon_id = coupon[0]['ID']
        coupon_code = coupon[0]['post_title']

    # Get coupon details with GET call
    coupon_details = apply_coupon_setup['coupons_api_helper'].call_retrieve_coupon(coupon_id)
    coupon_type = coupon_details['discount_type']
    discount = coupon_details['amount']
    coupon_expiration = coupon_details['date_expires']
    logger.info(f"Found coupon with discount amount: {discount} discount_type: {coupon_type}. Coupon expiration date: {coupon_expiration}")
    assert coupon_details['status'] == 'publish', f"Error. Coupon status: {coupon_details['status']}."
    assert apply_coupon_setup['generic_coupons_helper'].coupon_is_valid(coupon_id), f"Coupon is expired. Coupon expiration: {coupon_expiration}"


    # make api PUT call for order and add coupon_lines
    payload_update = {
        "coupon_lines": [{"code": coupon_code}]
    }
    update_response = apply_coupon_setup['orders_api_helper'].call_update_order(order_id, payload_update)
    total_after = update_response['total']
    logger.info(f"PUT response with coupon: {update_response}")
    logger.info(f"Order total after applying coupon: {total_after}")

    # verify coupon applied successfully
    apply_coupon_setup['generic_coupons_helper'].verify_coupon_successfully_applied(
        order_id=order_id,
        total_before=total_before,
        expected_discount=discount,
        coupon_id=coupon_id
    )

    # verify customer id in 'used_by' list of users for the coupon
    apply_coupon_setup['generic_coupons_helper'].verify_coupon_used_by_customer(coupon_id, customer_email, customer_id)