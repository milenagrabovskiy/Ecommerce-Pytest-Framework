"""Test suite for applying coupons to new orders.

This module provides fixtures and test cases to validate the correct
application of various coupon types (percent, fixed cart, fixed product,
and free coupon) to orders in the system. It ensures that:
- Orders are created correctly.
- Coupons are applied and reflected in the order totals.
- Customers are marked as having used the coupon.
- Only dynamically created coupons for fixed products are deleted after tests.
- Expired coupons do not apply to an order
"""
import pytest
import logging as logger
from demostore_automation.src.api_helpers.CouponAPIHelper import CouponAPIHelper
from demostore_automation.src.api_helpers.OrdersAPIHelper import OrdersAPIHelper
from demostore_automation.src.dao.coupons_dao import CouponsDAO
from demostore_automation.src.dao.customers_dao import CustomersDAO
from demostore_automation.src.generic_helpers.generic_coupons_helper import GenericCouponsHelper
from demostore_automation.src.dao.products_dao import ProductsDAO
from demostore_automation.src.generic_helpers.generic_orders_helper import GenericOrdersHelper
pytestmark = [pytest.mark.applycoupon]

@pytest.fixture(scope="module")
def apply_coupon_setup():
    """Fixture to set up a test environment for applying coupons.

    Returns:
        dict: Contains DAOs, API helpers, random product and customer,
              and lists for tracking created orders and coupons for teardown.
    """

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

@pytest.mark.smoke
@pytest.mark.parametrize(
    "discount_type",
    [
        pytest.param("percent", marks=pytest.mark.ebe8, id="apply_'percent'_coupon"),
        pytest.param("fixed_cart", marks=pytest.mark.ebe9, id="apply_'fixed_cart'_coupon"),
        pytest.param("fixed_product", marks=pytest.mark.ebe10, id="apply_'fixed_product'_coupon"),
        pytest.param("free_coupon", marks=pytest.mark.ebe11, id="apply_free_coupon")
    ]
)

def test_apply_coupon_to_new_order(apply_coupon_setup, discount_type):
    """Test applying a coupon to a newly created order.

    This test:
    1. Creates a new order for a random or fixed product.
    2. Retrieves or creates a coupon depending on the discount type.
    3. Applies the coupon to the order via API.
    4. Verifies that the order total and discount are correct.
    5. Checks that the customer is listed as having used the coupon.

    Args:
        apply_coupon_setup (dict): Fixture providing setup info and helpers.
        discount_type (str): Type of coupon to apply (percent, fixed_cart, fixed_product, free_coupon).

    Asserts:
        - Order total before and after applying coupon.
        - Discount applied matches expected.
        - Coupon is valid and published.
        - Customer is correctly listed as a coupon user.
    """

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
    order_response = apply_coupon_setup['generic_orders_helper'].create_order_for_customer(customer_id, product_id)
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

    # Fetch coupon from DB or create coupon for 'fixed_product' via helper method
    coupon_id, coupon_code = apply_coupon_setup["generic_coupons_helper"].get_coupon(
        discount_type, get_order, coupon_ids=apply_coupon_setup["coupon_ids"])

    # Get coupon details with GET call
    coupon_details = apply_coupon_setup['coupons_api_helper'].call_retrieve_coupon(coupon_id)
    coupon_type = coupon_details['discount_type']
    discount = coupon_details['amount']
    coupon_expiration = coupon_details['date_expires']
    logger.info(f"Found coupon with discount amount: {discount} discount_type: {coupon_type}. Coupon expiration date: {coupon_expiration}")
    assert coupon_details['status'] == 'publish', f"Error. Coupon status: {coupon_details['status']}."
    assert apply_coupon_setup['generic_coupons_helper'].is_coupon_valid(coupon_id), f"Coupon is expired. Coupon expiration: {coupon_expiration}"


    # make api PUT call for order and add coupon_lines
    update_response = apply_coupon_setup['generic_coupons_helper'].apply_coupon_to_order(coupon_code, order_id)
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

@pytest.mark.ebe12
def test_apply_expired_coupon_neg(apply_coupon_setup):
    """Verify that applying an expired coupon to an order fails.

    Creates an expired coupon, attempts to apply it to a new order,
    and checks that the API returns the correct error and that the coupon
    is recognized as invalid.

    Args:
        apply_coupon_setup (dict): Fixture with DAOs, API helpers, and test data.

    Asserts:
        - Coupon is expired.
        - API response matches expected error for expired coupons.
    """
    customer_id = apply_coupon_setup['customer_id']
    product_id = apply_coupon_setup['product_id']

    # create expired coupon
    expired_coupon = apply_coupon_setup["generic_coupons_helper"].create_expired_coupon()
    coupon_id = expired_coupon['id']
    apply_coupon_setup["coupon_ids"].append(coupon_id) # for teardown
    coupon_code = expired_coupon['code']

    # create order with expired coupon
    create_order = apply_coupon_setup["generic_orders_helper"].create_order_for_customer(customer_id, product_id)
    order_id = create_order['id']

    # try applying expired coupon
    update_response = apply_coupon_setup['generic_coupons_helper'].apply_coupon_to_order(coupon_code, order_id, expected_status_code=400)
    logger.info(f"update response for expired coupon: {update_response}")
    # verify coupon not valid
    assert not apply_coupon_setup["generic_coupons_helper"].is_coupon_valid(coupon_id), f"Error. Coupon expected to be expired."
    assert update_response ==  {'code': 'woocommerce_rest_invalid_coupon', 'message': 'This coupon has expired.', 'data': {'status': 400}}

@pytest.mark.ebe13
def test_apply_coupon_twice_neg(apply_coupon_setup):
    """Verify that applying the same coupon twice to one order does not change the discount or order total.

    Args:
        apply_coupon_setup (dict): Fixture with DAOs, API helpers, and test data.

    Asserts:
        - Order ID remains the same.
        - Discount and total do not change after second application.
        - Coupon code is identical for both applications.
    """
    customer_id = apply_coupon_setup['customer_id']
    product_id = apply_coupon_setup['product_id']

    order_response = apply_coupon_setup['generic_orders_helper'].create_order_for_customer(customer_id, product_id)
    order_id = order_response['id']

    coupon_id, coupon_code = apply_coupon_setup['generic_coupons_helper'].get_coupon(
        'percent', get_order=order_response, coupon_ids=apply_coupon_setup["coupon_ids"]
    )

    # apply coupon once
    apply_coupon = apply_coupon_setup['generic_coupons_helper'].apply_coupon_to_order(coupon_code, order_id)
    first_discount = float(apply_coupon['discount_total'])
    logger.info(f"first apply: {apply_coupon}")

    # apply coupon twice
    apply_coupon_twice = apply_coupon_setup['generic_coupons_helper'].apply_coupon_to_order(coupon_code, order_id)
    second_discount = float(apply_coupon_twice['discount_total'])
    logger.info(f"second apply response: {apply_coupon_twice}")

    # verify same coupon applied to same order and total did not change after second coupon
    assert apply_coupon['id'] == apply_coupon_twice['id'], f"Coupon applied to 2 different orders instead of same order."
    assert first_discount == second_discount, (f"Discount changed after applying the same coupon twice"
        f"First: {first_discount}, Second: {second_discount}")
    assert apply_coupon['total'] == apply_coupon_twice['total'], f"Order total changed after applying coupon second time."

    assert apply_coupon['coupon_lines'][0]['code'] == apply_coupon_twice['coupon_lines'][0]['code'], ("Different coupon codes used instead of applying same coupon twice."
                                                                                                      f"first coupon: {apply_coupon['coupon_lines'][0]['code']}"
                                                                                                      f"second coupon: {apply_coupon_twice['coupon_lines'][0]['code']}")