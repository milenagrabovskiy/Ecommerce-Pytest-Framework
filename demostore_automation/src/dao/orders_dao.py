"""Order Data Access Object (DAO) for retrieving WooCommerce order records from the database.

This module provides utility methods for fetching order information from the WordPress
database using raw SQL queries. It is primarily used for test validation in automation workflows.
"""

from demostore_automation.src.utilities.dbUtility import DBUtility
import logging as logger
import random

class OrdersDAO:
    """Handles database queries related to WooCommerce orders.

    This class uses `DBUtility` to connect and query the WordPress database
    for order information. It supports fetching orders by ID and randomly
    selecting orders for use in automated tests.
    """

    def __init__(self):
        self.db_helper = DBUtility()

    def get_order_by_id(self, order_id):
        """Fetch an order record from the database using its ID.

        Args:
            order_id (int): The ID of the order to retrieve.

        Returns:
            list[dict]: A list containing a single dictionary with the order's database fields.

        Raises:
            Exception: If the database query fails or no matching order is found.
        """
        sql = f"""
        SELECT * FROM {self.db_helper.database}.{self.db_helper.table_prefix}posts
        WHERE post_type = 'shop_order_placehold' AND ID = {order_id};
        """
        return self.db_helper.execute_select(sql)

    def get_random_order_by_status(self, status, qty=1):
        """Retrieve random orders filtered by status.
        Args:
            status (str): WooCommerce order status (e.g., 'processing', 'completed').
            qty (int, optional): Number of random orders to fetch. Defaults to 1.
        Returns:
            list[dict]: Random orders matching the specified status.
        """
        sql = f"""SELECT * FROM
        {self.db_helper.database}.{self.db_helper.table_prefix}wc_order_stats
        WHERE status = 'wc-{status}';"""
        rs_sql = self.db_helper.execute_select(sql)
        logger.info(f"Found {len(rs_sql)} orders with status {status}")
        return random.sample(rs_sql, int(qty))
