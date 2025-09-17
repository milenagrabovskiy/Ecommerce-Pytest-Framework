"""Test module for verifying WooCommerce order status updates.

This module covers creating orders via API, updating their status, and verifying the updates
through both API responses and database queries.

Test cases include:
- Updating to standard statuses: on-hold, completed, cancelled, refunded, failed, processing
- Verification of order integrity (ID and relevant fields) after status change
- Ensuring API and DB consistency for updated orders

Tests are parametrized using pytest.
"""
import pytest
import logging as logger


pytestmark = [pytest.mark.orders, pytest.mark.order_status]

@pytest.mark.parametrize(
     "order_status",
    [
        pytest.param("on-hold", marks=[pytest.mark.ebe47], id="update to on-hold"),
        pytest.param("completed", marks=[pytest.mark.ebe48, pytest.mark.smoke], id="update to completed"),
        pytest.param("cancelled", marks=[pytest.mark.ebe49], id="update to cancelled"),
        pytest.param("refunded",  marks=[pytest.mark.ebe51], id="update to refunded"),
        pytest.param("failed", marks=[pytest.mark.ebe50], id="update to failed"),
        pytest.param("processing", marks=[pytest.mark.ebe50], id="update to same status")
    ]
)

def test_change_order_status(my_orders_smoke_setup, order_status):
    """Test changing WooCommerce order status and verifying API and DB consistency.

    Steps:
    1. Create an order with default status 'processing'.
    2. Update the order to the specified `order_status`.
    3. Verify the update via the API response.
    4. Verify the order exists in the database with the correct updated status.
    5. For certain statuses (completed, cancelled, refunded), validate specific fields like
       'needs_payment', 'date_completed', and 'refunds'.

    Args:
        my_orders_smoke_setup (fixture): Fixture providing product info, API helpers, and teardown logic.
        order_status (str): The target status to update the order to (e.g., "completed", "refunded").

    Assertions:
        - The order status is correctly updated in the API response.
        - The order ID remains unchanged after update.
        - API and DB responses match for the updated order.
        - Relevant fields (like 'needs_payment' or 'date_completed') are correctly set for specific statuses.
    """
    # fetch product and customer
    # create order
    product_id = my_orders_smoke_setup["product_id"]
    product_price = my_orders_smoke_setup["product_price"]
    logger.info(f"Product ID: {product_id}, Product price: {product_price}")


    #create payload 'line_items' with custom product
    create_payload = {"status": "processing","line_items": [{"product_id": product_id}]}

    # make api call to create order
    create_order_responses = my_orders_smoke_setup["generic_orders_helper"].create_order(additional_args=create_payload)
    for create_order_response in create_order_responses:
        assert create_order_response, f"Create order API response is empty"

        order_id = create_order_response['id']

        # verify default order status == 'processing'
        assert create_order_response['status'] == 'processing', (f"Default order status should be 'processing',"
                                                                 f"Actual: {create_order_response['status']}")

        my_orders_smoke_setup["order_ids"].append(order_id) # keeps track of newly created order_id for teardown

        # make UPDATE call with new status
        update_payload = {"status": order_status}
        update_response = my_orders_smoke_setup["orders_api_helper"].call_update_order(order_id, payload=update_payload)
        logger.info(f"UPDATE api response after changing order_status: {update_response}")
        # verify order status
        assert update_response['status'] == order_status, (f"Order status after update call: {update_response['status']}"
                                                           f"Expected: {order_status}")
        # verify order is the same
        assert update_response['id'] == order_id, (f"Error. Wrong order_id after update api call. Expected: {order_id}"
                                                   f"Actual: {update_response['id']}")

        # verify newly updated order via GET api call and DB query
        get_response = my_orders_smoke_setup["generic_orders_helper"].verify_new_order_exists(order_id)
        logger.info(f"GET response: {get_response}")

        # verify correct status in API and DB, and for certain statuses (completed, cancelled, refunded),
        # check that specific fields like 'needs_payment', 'date_completed', and 'refunds' are correct
        my_orders_smoke_setup['generic_orders_helper'].verify_order_status(get_response, order_status)