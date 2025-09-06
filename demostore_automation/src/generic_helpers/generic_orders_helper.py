"""Helper module for creating and managing WooCommerce orders and notes.

Provides utilities to create orders with optional custom payloads, attach notes,
and verify existence of orders and notes via API and database.
"""
import logging as logger
import json
import os
from demostore_automation.src.api_helpers.OrdersAPIHelper import OrdersAPIHelper
from demostore_automation.src.dao.products_dao import ProductsDAO
from demostore_automation.src.dao.orders_dao import OrdersDAO


class GenericOrdersHelper:
    """Simplifies WooCommerce order creation and management.

    Attributes:
        orders_api_helper (OrdersAPIHelper): API helper for orders.
        products_dao (ProductsDAO): Access to product data.
        current_file_dir (str): Path to the current file directory.
    """
    def __init__(self):
        self.orders_api_helper = OrdersAPIHelper()
        self.products_dao = ProductsDAO()
        self.orders_dao = OrdersDAO()
        self.current_file_dir = os.path.dirname(os.path.realpath(__file__))


    def create_order(self, order_qty=1, product_qty=1, additional_args=None):
        """Create an order with optional custom arguments.

        Args:
            additional_args (dict, optional): Fields to override or add to the order payload.
            order_qty (int): Quantity of orders.
            product_qty (int): Quantity of products.

        Returns:
            dict: API response with the created order details.

        Raises:
            TypeError: If `additional_args` is not a dict.
            FileNotFoundError, IOError, PermissionError, UnicodeError: File read errors.
        """
        # Create full path regardless of os
        payload_json_file = os.path.join(self.current_file_dir, '..', 'data', 'create_order_payload.json')

        try:
            with open(payload_json_file, 'r') as f:
                payload = json.load(f)

            if additional_args:
                if not isinstance(additional_args, dict):
                    raise TypeError(f"File must be of type dict. Actual: {type(additional_args)}")
                payload.update(additional_args)

            if "line_items" not in payload:
                random_product = self.products_dao.get_random_product_from_db(qty=1)
                random_product_id = random_product[0]['ID']
                payload["line_items"] = [{"product_id": random_product_id, "quantity": product_qty}]

            else:
                for i in payload["line_items"]:
                    i["quantity"] = product_qty # if not line_items, payload will still take product_qty


        except (FileNotFoundError, IOError, PermissionError, UnicodeError) as e:
            logger.error(f"Could not read payload file: {e}")
            raise

        create_order_responses = []
        for i in range(order_qty):
            create_order_response = self.orders_api_helper.call_create_order(payload=payload)
            create_order_responses.append(create_order_response)
            logger.info(f"Created order: {create_order_response}")

        return create_order_responses


    def verify_new_order_exists(self, order_id):
        """Verify that a newly created order exists in API and database.

        Args:
            order_id (int): ID of the order to verify.

        Raises:
            AssertionError: If order is missing or ID mismatches in API or DB.

        Returns:
            GET api response
        """
        # API check
        get_order_response = self.orders_api_helper.call_retrieve_order(order_id)
        assert get_order_response['id'] == order_id, (f"Get order by id api response returned wrong order id."
                                                      f"Actual: {get_order_response['id']}, Expected: {order_id}")
        logger.info(f"GET api call for order by id successfully found new order")

        # DB check
        db_order = self.orders_dao.get_order_by_id(order_id)
        assert db_order, "DB query for fetching order by id is empty"
        assert db_order[0]['ID'] == order_id, f"DB query for fetching order by id returned wrong order id. Actual: {db_order[0]['ID']}, Expected: {order_id}"
        logger.info("DB query for fetching order by id successfully found new order")

        return get_order_response

    def create_order_for_customer(self, customer_id, product_id):
        """Create an order for a specific customer and product with free shipping.

        Args:
            customer_id (int): ID of the customer.
            product_id (int): ID of the product.

        Returns:
            dict: API response for the created order.
        """
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
        return self.create_order(additional_args=product_args)


    def create_order_note(self, order_id, qty=1, payload=None):
        """Create one or more notes for an order.

        Args:
            order_id (int): Order ID to attach the note(s) to.
            qty (int, optional): Number of notes to create. Defaults to 1.
            payload (dict, optional): Note payload, e.g., {"note": "text"}. Defaults to {"note": "Automation test note"}.

        Returns:
            list[dict]: List of API responses for each created note.

        Raises:
            TypeError: If payload is not a dictionary.
        """
        if not payload:
            payload = {
                "note": "Automation test note"
            }
        if not isinstance(payload, dict):
            raise TypeError(f"Payload must be of type dict. Actual: {type(payload)}")
        responses = []
        for i in range(qty):
            note_api_response = self.orders_api_helper.call_create_order_note(order_id, payload=payload)
            responses.append(note_api_response)
            logger.info(f"Created order note: {note_api_response}")
        return responses

    def verify_note_exists(self, order_id, note_id, note_text):
        """Verify that a specific order note exists in API and database.

        Args:
            order_id (int): Order ID the note belongs to.
            note_id (int): ID of the note to verify.
            note_text (str): Expected text of the note.

        Raises:
            AssertionError: If note does not exist in API or database, or IDs mismatch.
        """
        get_note_response = self.orders_api_helper.call_retrieve_order_note(order_id, note_id)
        assert get_note_response['id'] == note_id, (f"Get order note response returned wrong note id."
                                                    f"Actual: {get_note_response['id']}, Expected: {note_id}")
        logger.info(f"GET api call for order note by note id successfully found new order note")

        db_orders_with_note_text = self.orders_dao.get_orders_by_note_text(note_text)
        for i in db_orders_with_note_text:
            if i['comment_ID'] == note_id:
                break
        else:
            raise AssertionError(f"Note id {note_id} for created note is not found in the DB")

    def verify_order_status(self, get_response, order_status):
        """Verify that the order status is correct in both API response and database.

        Also checks additional fields for specific statuses:
          - 'completed': ensures 'date_completed' is set.
          - 'cancelled' or 'refunded': ensures 'needs_payment' is False.
          - 'refunded': validates refund details ('reason' and 'total').

        Args:
            get_response (dict): API response for the order.
            order_status (str): Expected order status (e.g., 'completed', 'refunded').

        Raises:
            AssertionError: If any check fails.
        """
        order_id = get_response['id']
        assert get_response['status'] == order_status
        db_details = self.orders_dao.get_order_status_by_id(order_id)
        assert db_details[0]['status'].endswith(order_status), (f"Wrong status in DB. Actual: {db_details[0]['status']}"
                                                                f"Expected: {order_status}")
        if order_status in ["completed", "cancelled", "refunded"]:
            assert not get_response['needs_payment'], (f"Error. 'needs_payment' expected to be 'False'"
                                                       f"for order status:{order_status} but returned 'True'")

        if order_status == 'completed':
            assert get_response['date_completed'], ("GET api response returned empty for"
                                                    "'date_completed' field for order_status: completed")

        if order_status == 'refunded':
            assert get_response['refunds'], (f"Error. 'refunds' field is empty after refunding order."
                                             f"Should contain order id: {order_id}")
            assert get_response['refunds'][0]['reason'], 'Missing refund message in "refunds" field'
            assert get_response['refunds'][0]['total'] == f"-{get_response['total']}", (f"Refund total does not match order total."
                                                                                     f"Actual: {get_response['refunds']['total']}"
                                                                                     f"Expected: -{get_response['total']}")


    def create_order_refund(self, order_response, refund_type, additional_args=None):
        order_id = order_response['id']
        order_total = float(order_response['total'])
        if refund_type == 'full':
            refund_amount = order_response['total']
        elif refund_type == 'partial': # half refund
            refund_amount = round(order_total / 2, 2)
        elif refund_type == 'refund_1_product':
            refund_amount = float(order_response['line_items'][0]['price'])

        refund_payload = {
            "amount": str(refund_amount),  # total refund amount
            "line_items": [
                {
                    "id": order_response['line_items'][0]['id'],
                    "quantity": 1  # instead of refund_total
                }
            ],
            "refund_payment": False
        }
        response = self.orders_api_helper.call_create_refund(
            order_id=order_id,
            payload=refund_payload
        )
        return response


