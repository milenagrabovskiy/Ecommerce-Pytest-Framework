"""Helper module for creating and managing WooCommerce orders.

Provides functions to create orders with optional custom payloads,
automatically select random products if none are specified, and verify
that newly created orders exist both via the API and in the database.
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
        # create full path regardless of os
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