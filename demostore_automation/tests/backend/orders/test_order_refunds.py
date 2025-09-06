import pytest
import logging as logger
from demostore_automation.tests.backend.orders.test_create_order_smoke import my_orders_smoke_setup

pytestmark = [pytest.mark.orders, pytest.mark.order_refund]

@pytest.mark.xfail(reason=" Response Json: {'code': 'woocommerce_rest_cannot_create_order_refund',"
                          "'message': 'The payment gateway for this order does not support automatic refunds.', 'data': 500}")
@pytest.mark.order_status_edge
@pytest.mark.parametrize(
     "refund_type",
    [
        pytest.param("full", marks=[pytest.mark.ebe47], id="update to same status"),
        pytest.param("partial", marks=[pytest.mark.ebe48, pytest.mark.smoke], id="update to empty string"),
        pytest.param("refund_1_product", marks=[pytest.mark.ebe49], id="update to random string")
    ]
)

def test_order_refund(my_orders_smoke_setup, refund_type):
    # fetch product and customer
    # create order
    product_id = my_orders_smoke_setup["product_id"]
    product_price = my_orders_smoke_setup["product_price"]
    logger.info(f"Product ID: {product_id}, Product price: {product_price}")


    #create payload 'line_items' with custom product
    # create_payload = {"status": "processing","line_items": [{"product_id": product_id}]}
    create_payload = {
        "status": "processing",
        "payment_method": "bacs",
        "payment_method_title": "bacs",
        "line_items": [{"product_id": product_id}]
    }
    # make api call to create order
    product_qty = 2 if refund_type == 'refund_1_product' else 1
    create_order_responses = my_orders_smoke_setup["generic_orders_helper"].create_order(additional_args=create_payload,
                                                                                         product_qty=product_qty)
    for create_order_response in create_order_responses:
        assert create_order_response, f"Create order API response is empty"

        order_id = create_order_response['id']

        my_orders_smoke_setup["order_ids"].append(order_id) # keeps track of newly created order_id for teardown

        # make UPDATE call with refund
        update_response = (my_orders_smoke_setup['generic_orders_helper'].create_order_refund(order_response=create_order_response,
                                                                                              refund_type=refund_type))

        logger.info(f"Update response: {update_response}")

        # calculate expected refund amount
        if refund_type == "full":
            expected_amount = float(create_order_response['total'])
        elif refund_type == "partial":
            expected_amount = round(float(create_order_response['total']) / 2, 2)
        elif refund_type == "refund_1_product":
            expected_amount = float(create_order_response['line_items'][0]['price'])

        # assert against API response
        assert float(update_response["amount"]) == expected_amount, (
            f"Incorrect refund amount after update call. Expected: {expected_amount}, "
            f"Actual: {update_response['amount']}"
        )

