"""Tests for creating WooCommerce order notes for guest and registered users.

Covers:
- Creating orders with single or multiple notes.
- Validating note creation via API and database.
- Automatic cleanup of orders and notes after tests.
"""
import pytest
import logging as logger
from demostore_automation.src.api_helpers.OrdersAPIHelper import OrdersAPIHelper
from demostore_automation.src.dao.customers_dao import CustomersDAO
from demostore_automation.src.dao.products_dao import ProductsDAO
from demostore_automation.src.generic_helpers.generic_orders_helper import GenericOrdersHelper

@pytest.fixture(scope="module")
def order_notes_setup():
    """Set up DAOs, helpers, a random product, default note text, and track created orders."""
    orders_api_helpers = OrdersAPIHelper()
    products_dao = ProductsDAO()
    customers_dao = CustomersDAO()
    generic_orders_helper = GenericOrdersHelper()

    # fetch random product from db
    product = products_dao.get_random_product_from_db(qty=1)[0]
    product_id = product["ID"]

    info = {
        "orders_api_helpers": orders_api_helpers,
        "products_dao": products_dao,
        "customers_dao": customers_dao,
        "generic_orders_helper": generic_orders_helper,
        "product_id": product_id,
        "note_text": "Automation test note",
        "order_ids": []
    }

    yield info

    # deleting order automatically deletes the order note(s)
    for order_id in info["order_ids"]:
        orders_api_helpers.call_delete_order(order_id)
        logger.info(f"Deleted order id: {order_id} and all order notes")
    logger.info(f"Successfully deleted {len(info['order_ids'])} orders")


@pytest.mark.parametrize(
    "user_type, quantity",
    [
        pytest.param("guest_user", 1, marks=[pytest.mark.ecomnotes, pytest.mark.ecomnotes1], id="guestuser_1_note"),
        pytest.param("guest_user", 5, marks=[pytest.mark.ecomnotes, pytest.mark.ecomnotes1], id="guestuser_5_notes"),
        pytest.param("registered_user", 1, marks=[pytest.mark.ecomnotes, pytest.mark.ecomnotes2], id="reg_user_1_notes"),
        pytest.param("registered_user", 5, marks=[pytest.mark.ecomnotes, pytest.mark.ecomnotes2], id="reg_user_5_notes")
    ]
)
@pytest.mark.ordernotes
def test_create_order_note(order_notes_setup, user_type, quantity):
    """Test creating one or multiple order notes for a given user type.

    Args:
        order_notes_setup (dict): Fixture providing DAOs, helpers, product ID, note text, and order tracking.
        user_type (str): 'guest_user' or 'registered_user'.
        quantity (int): Number of notes to create.
    """
    # determine 'user_type'
    if user_type == "registered_user":
        customer = order_notes_setup["customers_dao"].get_random_customer_from_db(qty=1)[0]
        customer_id = customer["ID"]
    else:
        customer_id = 0

    # create order with product and quantity
    order_payload = {
        "customer_id": customer_id,
        "line_items": [{"product_id": order_notes_setup["product_id"], "quantity": quantity}]
    }
    order_list = order_notes_setup["generic_orders_helper"].create_order(additional_args=order_payload)

    for order in order_list: # helper method returns a list
        order_id = order["id"]
        order_notes_setup["order_ids"].append(order_id)
        logger.info(f"Created order {order_id} for {user_type} (customer {customer_id})")

        # add order note
        note_payload = {"note": order_notes_setup["note_text"]}

        create_note_responses = order_notes_setup["generic_orders_helper"].create_order_note(
            order_id, qty=quantity, payload=note_payload)

        for create_note_response in create_note_responses:
            assert create_note_response, "API response for create order note is empty"
            assert create_note_response["note"] == order_notes_setup["note_text"], (f"Create order note response note text not as expected."
                                                                                    f"Expected: {order_notes_setup['note_text']}"
                                                                                    f"Actual: {create_note_response['note']}")
            note_id = create_note_response["id"]
            assert note_id, "Create order note response did not return note_id"
            assert not create_note_response["customer_note"], "customer_note field expected to be 'False' but returned 'True'"

            # verify newly create note exists via API and in DB
            order_notes_setup["generic_orders_helper"].verify_note_exists(order_id, note_id, note_text=order_notes_setup["note_text"])
        assert len(create_note_responses) == quantity, (f"Quantity of notes created does not match expected."
                                                        f"Expected: {quantity}, Actual: {len(create_note_responses)}")
        logger.info(f"Created {len(create_note_responses)} notes")