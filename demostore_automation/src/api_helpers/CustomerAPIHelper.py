"""WooCommerce Customer API helper module.

Provides helper methods for interacting with WooCommerce customer endpoints;
"""

from demostore_automation.src.utilities.wooAPIUtility import WooAPIUtility


class CustomerAPIHelper:
    """Helper for performing WooCommerce customer API operations.

    Attributes:
        woo_api_utility (WooAPIUtility): Instance used to make WooCommerce API requests.
    """

    def __init__(self):
        self.woo_api_utility = WooAPIUtility()

    def call_delete_customer(self, customer_id, force=True):
        """Delete a WooCommerce customer via API.

        WooCommerce does not support trashing customers. This method permanently deletes
        the customer when `force=True`.

        Args:
            customer_id (int): The ID of the customer to delete.
            force (bool, optional): Whether to permanently delete the customer. Defaults to True.

        Returns:
            dict: Response from the WooCommerce API.
        """
        return self.woo_api_utility.delete(f"customers/{customer_id}", params={"force": force})
