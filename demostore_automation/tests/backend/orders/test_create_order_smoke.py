"""Smoke tests for the WooCommerce Orders API.

This module includes setup fixtures for fetching a random product and creating orders.
It ensures cleanup of created orders after tests. Supports order creation for both
guest and registered users, verifying the API response and database consistency.
"""
import pytest
import re
import logging as logger

from demostore_automation.src.api_helpers.OrdersAPIHelper import OrdersAPIHelper
from demostore_automation.src.api_helpers.ProductsAPIHelper import ProductsAPIHelper
from demostore_automation.src.dao.customers_dao import CustomersDAO
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


@pytest.mark.parametrize(
     "user_type, quantity",
    [
        pytest.param("guest_user", 1, marks=[pytest.mark.orders, pytest.mark.ecomorders1]),
        pytest.param("guest_user", 5, marks=[pytest.mark.orders, pytest.mark.ecomorders1]),
        pytest.param("registered_user", 1, marks=[pytest.mark.orders, pytest.mark.ecomorders2]),
        pytest.param("registered_user", 5, marks=[pytest.mark.orders, pytest.mark.ecomorders2])
    ]
)

def test_create_order(my_orders_smoke_setup, user_type, quantity):
    """Verify that orders can be created and retrieved via the WooCommerce API.

    Creates an order for a guest or registered user and asserts the following:
        - API response is not empty.
        - Order ID is an integer.
        - Customer ID matches expected value (0 for guest, or the correct customer ID).
        - Order key format starts with 'wc_order_'.
        - Newly created order can be retrieved via API and exists in the database.

    Args:
        my_orders_smoke_setup (dict): Fixture providing product info, API helpers, and order tracking.
        user_type (str): Type of user creating the order, either "guest_user" or "registered_user".
    """
    product_id = my_orders_smoke_setup["product_id"]
    product_price = my_orders_smoke_setup["product_price"]
    logger.info(f"Product ID: {product_id}, Product price: {product_price}")


    #overwrite 'line_items' with custom product(s)
    product_args = {"line_items": [{"product_id": product_id, "quantity": quantity}]}
    logger.info(f"Product quantity in line_items: {quantity}")
    if user_type == "registered_user":
        customers_dao = CustomersDAO()
        random_customer = customers_dao.get_random_customer_from_db(qty=1)[0]
        expected_customer_id = random_customer['ID']
        product_args.update({"customer_id": random_customer['ID']})
        logger.info(f"Fetched random customer from database with id: {expected_customer_id}")
    else:
        expected_customer_id = 0

    # make api call and verify it is not empty
    create_order_response = my_orders_smoke_setup["generic_orders_helper"].create_order(additional_args=product_args)
    assert create_order_response, f"Create order as guest user API response is empty"

    # verify customer id
    assert create_order_response['customer_id'] == expected_customer_id, \
        f"Incorrect customer id in api response. Expected: {expected_customer_id}, Actual: {create_order_response['customer_id']}"

    # verify order_id is an int
    order_id = create_order_response['id']
    assert isinstance(order_id, int), f"Create order as guest user order_id must be of type int. Actual: {type(order_id)}"

    my_orders_smoke_setup["order_ids"].append(order_id) # keeps track of newly created order_id for teardown

    # assert order key starts with 'wc_order_'
    assert re.match(r"^wc_order_.+", create_order_response["order_key"]), \
        f"Order key is invalid. Must start with 'wc_order_' Got: {create_order_response['order_key']}"

    logger.info(f"Successfully created order as {user_type} user")

    # verify new order via GET api call and DB query
    my_orders_smoke_setup["generic_orders_helper"].verify_new_order_exists(order_id)


@pytest.mark.ecomorders3
def test_create_order_no_payment_info(my_orders_smoke_setup):
    """Verify order creation with missing billing, shipping, and payment data.

    Ensures the API still creates an order when critical fields are empty and
    sets the correct flags and status.

    Args:
        my_orders_smoke_setup (dict): Fixture with product info, API helpers,
            and order tracking.

    Asserts:
        - Response is not empty.
        - Order ID is generated and tracked for teardown.
        - `needs_processing` is True.
        - `needs_payment` is True.
        - Status equals "pending".
    """
    product_id = my_orders_smoke_setup["product_id"]
    product_price = my_orders_smoke_setup["product_price"]
    logger.info(f"Product ID: {product_id}, Product price: {product_price}")

    product_args = {
                    "line_items": [{"product_id": product_id, "quantity": 1}],
                    "shipping": {},
                    "billing": {},
                    "shipping_lines": {},
                    "set_paid": False,
                    "payment_method": '',
                    "payment_method_title": ''
                    }

    create_order_response = my_orders_smoke_setup["generic_orders_helper"].create_order(additional_args=product_args)
    assert create_order_response, f"Create order as guest user API response is empty"
    order_id = create_order_response['id']
    my_orders_smoke_setup["order_ids"].append(order_id)
    assert create_order_response["needs_processing"], (f"Create order without billing, shipping, and payment info returned"
                                                     f" 'False' for 'needs_processing'")
    assert create_order_response["needs_payment"], (f"Create order without billing, shipping, and payment info returned"
                                                    f" 'False' for 'needs_payment'")
    assert create_order_response["status"] == "pending", (f"Create order without billing, shipping, and payment info"
                                                                                f"returned wrong order status: {create_order_response['status']}")

@pytest.mark.ecomorders4
def test_create_order_empty_line_items_negative(my_orders_smoke_setup):
    """Verify that an order can be created without products (empty line_items).

    WooCommerce allows order creation without mandatory product fields.
    This test ensures:
      - The order is created with an empty `line_items` list.
      - The order status is returned as "completed".

    Args:
        my_orders_smoke_setup (fixture): Provides API helpers and teardown tracking.
    """
    product_args = {"line_items": []}
    create_order_response = my_orders_smoke_setup["generic_orders_helper"].create_order(additional_args=product_args)
    order_id = create_order_response['id']
    my_orders_smoke_setup["order_ids"].append(order_id) # for teardown
    logger.info(f"Create order api response without line_items: {create_order_response}")


    # There are no mandatory fields for creating order via api. Woocommerce api allows order creation without products.
    # Expected status code is 201 (verification done in 'OrdersAPIHelper().call_create_order()')

    assert not create_order_response["line_items"], (f"Create order with no product(s) expected to return empty 'line_items'."
                                                     f"Actual: {create_order_response['line_items']}")
    assert create_order_response["status"] == "completed", f"Create order with no product(s) expected to return order status 'completed'. Actual: {create_order_response['status']}"
