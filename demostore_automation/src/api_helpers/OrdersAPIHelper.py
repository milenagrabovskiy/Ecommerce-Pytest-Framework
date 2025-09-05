"""Orders API Helper.

This module provides a helper class to interact with the WooCommerce
Orders API, including creating, retrieving, updating, and deleting orders and order notes.
"""
from demostore_automation.src.utilities.wooAPIUtility import WooAPIUtility


class OrdersAPIHelper:
    """Helper class to interact with WooCommerce orders via API.

    Initializes a WooAPIUtility instance to perform API calls related to orders.
    """

    def __init__(self):
        self.woo_api_utility = WooAPIUtility()


    def call_create_order(self, payload):
        """Creates a new order using the WooCommerce API.

        Args:
            payload (dict): The order data to send in the API request.
            expected_status_code (int, optional): The expected HTTP status code for a successful creation. Defaults to 201.

        Returns:
            dict: The JSON response from the API representing the created order.
        """
        return self.woo_api_utility.post("orders", params=payload, expected_status_code=201)

    def call_retrieve_order(self, order_id):
        """Retrieves order details by order ID.

        Args:
            order_id (int or str): The ID of the order to retrieve.

        Returns:
            dict: The JSON response from the API representing the retrieved order.
        """
        return self.woo_api_utility.get(f'orders/{order_id}', expected_status_code=200)

    def call_delete_order(self, order_id):
        """Deletes an order by order ID.

        Args:
            order_id (int or str): The ID of the order to delete.

        Returns:
            dict: The JSON response from the API after deleting the order.
        """
        return self.woo_api_utility.delete(f'orders/{order_id}', expected_status_code=200)

    def call_update_order(self, order_id, payload, expected_status_code=200):
        """Updates existing order using the WooCommerce API.

        Args:
            payload (dict): The order data to send in the API request.
            expected_status_code (int, optional): The expected HTTP status code for a successful update. Defaults to 200.

        Returns:
            dict: The JSON response from the API representing the updated order.
        """
        return self.woo_api_utility.put(f"orders/{order_id}", params=payload, expected_status_code=expected_status_code)


    def call_create_order_note(self, order_id, payload):
        """Create a note for a specific order.

        Args:
            order_id (int or str): ID of the order.
            payload (dict): Note data to send in the API request.

        Returns:
            dict: JSON response representing the created note.
        """
        return self.woo_api_utility.post(f'orders/{order_id}/notes', params=payload, expected_status_code=201)

    def call_retrieve_order_note(self, order_id, note_id):
        """Retrieve a specific note from an order.

        Args:
            order_id (int or str): ID of the order.
            note_id (int or str): ID of the note.

        Returns:
            dict: JSON response with the order note details.
        """
        return self.woo_api_utility.get(f'orders/{order_id}/notes/{note_id}')

    def call_delete_order_note(self, order_id, note_id, params=None):
        """Delete a specific note from an order.

        Args:
            order_id (int or str): ID of the order.
            note_id (int or str): ID of the note to delete.
            params (dict, optional): Additional request parameters. Defaults to None.

        Returns:
            dict: JSON response after deleting the note.
        """
        return self.woo_api_utility.delete(f'orders/{order_id}/notes/{note_id}', params=params)


