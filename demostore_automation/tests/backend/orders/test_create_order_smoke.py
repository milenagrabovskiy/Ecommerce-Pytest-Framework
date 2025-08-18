"""Smoke tests for WooCommerce order API.

Includes setup fixtures for fetching random products and ensures
cleanup of created orders after tests. Supports tests for various
order creation scenarios.
"""
import pytest
import re
import logging as logger

from demostore_automation.src.api_helpers.OrdersAPIHelper import OrdersAPIHelper
from demostore_automation.src.api_helpers.ProductsAPIHelper import ProductsAPIHelper
from demostore_automation.src.dao.products_dao import ProductsDAO
from demostore_automation.src.generic_helpers.generic_orders_helper import GenericOrdersHelper

@pytest.fixture(scope="module")
def my_orders_smoke_setup():
    """Setup fixture for creating and cleaning up test orders.

    Fetches a random product from the database and prepares API helpers.
    Tracks created orders for teardown after tests complete.

    Yields:
        dict: {
            "product_id" (int): Random product ID from DB,
            "product_price" (float): Product price,
            "orders_api_helper" (OrdersAPIHelper): Helper for order API calls,
            "order_ids" (list[int]): Tracks created order IDs for teardown
        }
    """
    products_dao = ProductsDAO()
    product_api_helper = ProductsAPIHelper()
    random_product = products_dao.get_random_product_from_db(qty=1)[0]
    product_id = random_product['ID']
    logger.info(f"Fetched random product from DB: {random_product}")
    product_details = product_api_helper.call_get_product_by_id(product_id)
    product_price = product_details['price']
    info = {
        "product_id": random_product['ID'],
        "product_price": product_price,
        "orders_api_helper": OrdersAPIHelper(),
        "generic_orders_helper": GenericOrdersHelper(),
        "order_ids": []
    }
    yield info

    for ord_id in info["order_ids"]:
        info["orders_api_helper"].call_delete_order(ord_id)
        logger.info(f"Successfully deleted order id: {ord_id}")

@pytest.mark.ecom_orders1
def test_create_order_guest_user(my_orders_smoke_setup):
    """Verify an order can be created and retrieved via API.

    Checks that the order creation response is valid, order ID is an integer,
    customer ID is correct, and order key format is valid. Also ensures the
    order can be retrieved by ID.

    Args:
        my_orders_smoke_setup (dict): Fixture providing product info and API helpers.

    Asserts:
        - API response is not empty.
        - Order ID is an integer.
        - Customer ID is correct (0 for guest orders, otherwise appropriate).
        - Order key has valid format.
        - Retrieved order matches created order ID.
    """
    product_id = my_orders_smoke_setup["product_id"]
    product_price = my_orders_smoke_setup["product_price"]
    logger.info(f"Product ID: {product_id}, Product price: {product_price}")

    #overwrite 'line_items' with custom product(s)
    product_args = {"line_items": [{"product_id": product_id, "quantity": 1}]}

    # make api call and verify it is not empty
    create_order_response = my_orders_smoke_setup["generic_orders_helper"].create_order(additional_args=product_args)
    assert create_order_response, f"Create order as guest user API response is empty"

    # verify order_id is an int
    order_id = create_order_response['id']
    assert isinstance(order_id, int), f"Create order as guest user order_id must be of type int. Actual: {type(order_id)}"

    my_orders_smoke_setup["order_ids"].append(order_id) # keeps track of newly created order_id for teardown

    customer_id = create_order_response['customer_id']
    assert customer_id == 0, f"Create order as guest user should have customer_id of 0. Actual {customer_id}"

    # assert order key starts with 'wc_order_'
    assert re.match(r"^wc_order_.+", create_order_response["order_key"]), \
        f"Order key is invalid. Must start with 'wc_order_' Got: {create_order_response['order_key']}"

    logger.info("Successfully created order as guest user")

    # verify new order via GET api call and DB query
    my_orders_smoke_setup["generic_orders_helper"].verify_new_order_exists(order_id)