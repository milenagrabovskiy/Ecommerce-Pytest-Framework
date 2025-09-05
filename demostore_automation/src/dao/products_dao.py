"""Product Data Access Object (DAO) for retrieving WooCommerce product records from the database.

This module provides utility methods for fetching product information from the WordPress
database using raw SQL queries. It is primarily used for test validation in automation workflows.
"""

from demostore_automation.src.utilities.dbUtility import DBUtility
import random
import logging as logger

class ProductsDAO:
    """Handles database queries related to WooCommerce products.

    This class uses `DBUtility` to connect and query the WordPress database
    for product information. It supports fetching products by ID and randomly
    selecting products for use in automated tests.
    """

    def __init__(self):
        self.db_helper = DBUtility()

    def get_random_product_from_db(self, qty=1):
        """Fetch a specified number of random products from the database.

        Args:
            qty (int): The number of random products to retrieve. Defaults to 1.

        Returns:
            list[dict]: A list of product records, each as a dictionary containing fields
            such as `ID`, `post_title`, and `post_name`.

        Raises:
            ValueError: If `qty` exceeds the number of available products in the query result.
        """

        logger.info(f"Getting random products from db. qty= {qty}")
        sql = f"""SELECT ID, post_title, post_name FROM {self.db_helper.database}.{self.db_helper.table_prefix}posts 
        WHERE post_type = 'product' AND post_status = 'publish' LIMIT 500;"""

        rs_sql = self.db_helper.execute_select(sql)

        return random.sample(rs_sql, int(qty))


    def get_product_by_id(self, product_id):
        """Fetch a product record from the database using its ID.

        Args:
            product_id (int): The ID of the product to retrieve.

        Returns:
            list[dict]: A list containing a single dictionary with the product's database fields.

        Raises:
            Exception: If the database query fails or no matching product is found.
        """
        sql = f"""SELECT * FROM {self.db_helper.database}.{self.db_helper.table_prefix}posts 
        WHERE post_type = 'product' AND ID = {product_id};"""

        return self.db_helper.execute_select(sql)


    def get_product_price(self, product_id):
        """Fetch the price-related meta fields of a product from the database.

        Args:
            product_id (int): ID of the product.

        Returns:
            list[dict]: List of dictionaries with 'meta_key' and 'meta_value'
                        for '_regular_price', '_sale_price', and '_price'.
        """
        sql = f""" SELECT * FROM {self.db_helper.database}.{self.db_helper.table_prefix}postmeta
        WHERE post_id = {product_id} AND meta_key IN ('_regular_price', '_sale_price', '_price');
        """
        return self.db_helper.execute_select(sql)