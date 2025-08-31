"""GenericProductsHelper module.

Provides a helper class to create WooCommerce products via API and verify their existence
in both the API and the database.

Class:
    GenericProductsHelper: Contains methods to create products of various types
    and verify them in API and database.

Methods:
    GenericProductsHelper.create_product_by_type: Create a product with optional attributes.
    GenericProductsHelper.verify_product_is_created: Verify that a product exists in API and database.
"""
import logging as logger
from demostore_automation.src.api_helpers.ProductsAPIHelper import ProductsAPIHelper
from demostore_automation.src.dao.products_dao import ProductsDAO
from demostore_automation.src.utilities.genericUtilities import generate_random_string


class GenericProductsHelper:
    """Helper for creating and verifying WooCommerce products.

    Initializes API and database access helpers for product creation and verification.

    Attributes:
        products_dao (ProductsDAO): Database access for products.
        products_api_helper (ProductsAPIHelper): API access for product endpoints.
    """

    def __init__(self):
        self.products_dao = ProductsDAO()
        self.products_api_helper = ProductsAPIHelper()

    def create_product_by_type(self, product_type, additional_args=None):
        """Create a product of a given type with optional attributes.

        Args:
            product_type (str): Product type ('simple', 'variable', 'grouped', 'external').
            additional_args (dict, optional): Additional fields for product creation.

        Returns:
            dict: WooCommerce API response.

        Raises:
            TypeError: If additional_args is not a dict.
        """
        name = generate_random_string(prefix=product_type)
        payload = {
            "name": name,
            "type": product_type,
            "regular_price": "20.00",
        }

        if product_type == "variable" and additional_args is None:
            additional_args = {
                "attributes": [
                  {
                    "name": "Size",
                    "visible": True,
                    "variation": True,
                    "options": ["option1", "option2"]
                  }
                ]
            }

        elif product_type == "grouped" and additional_args is None:
            db_products = self.products_dao.get_random_product_from_db(3)
            db_product_ids = [product['ID'] for product in db_products] # list comprehension to collect product ids from db

            additional_args = {
                "grouped_products": db_product_ids  # IDs of simple products to include since grouped products are all type simple
            }

        elif product_type == "external" and additional_args is None:
            additional_args = {
                "external_url": "https://example.com/product",
                "button_text": "Button"
            }

        if additional_args:
            if not isinstance(additional_args, dict):
                logger.error(f"additional_args must be of type dict, Actual: {type(additional_args)}")
                raise TypeError
            payload.update(additional_args)
        post_response = self.products_api_helper.call_create_product(payload=payload)
        return post_response


    def verify_product_is_created(self, post_response):
        """Verify that a product exists in the API and database.

        Args:
            post_response (dict): Response from create_product_by_type.

        Raises:
            AssertionError: If the product is missing or fields mismatch.
        """
        # POST api call assertions
        assert post_response, "Create product POST api call is empty."

        assert post_response['status'] == 'publish', (f"Create a simple product POST api call response"
                                                       f"returned unexpected 'status'"
                                                       f"Expected: 'publish', Actual: {post_response['status']}")

        # make GET api call to verify product exists
        product_type = post_response['type']
        product_id = post_response['id']
        product_name = post_response['name']
        get_response = self.products_api_helper.call_get_product_by_id(product_id)

        # GET api call assertions
        assert get_response, f"Create a {product_type} product GET api call is empty."

        assert get_response['id'] == product_id, (f"Create a {product_type} product GET api call response"
                                                       f"returned wrong product id"
                                                       f"Expected: {product_id}, Actual: {get_response['id']}")

        assert get_response['type'] == product_type, (f"Create a {product_type} product GET api call response"
                                                       f"returned unexpected 'product_type'"
                                                       f"Expected: {product_type}, Actual: {get_response['product_type']}")
        assert get_response['name'] == product_name, (f"Create a {product_type} product GET api call response"
                                                       f"returned wrong product name"
                                                       f"Expected: {product_name}, Actual: {get_response['name']}")
        if get_response['virtual'] or get_response['downloadable']:
            assert product_type == "simple", f"Virtual or Downloadable products must be of type 'simple'. Actual: {product_type}"

        if product_type == "external":
            assert get_response["button_text"] == post_response["button_text"]
            assert get_response["external_url"] == post_response["external_url"]

        if product_type == "grouped":
            assert get_response['grouped_products'] and len(get_response['grouped_products']) > 1, (f"Grouped products must be present and have more than one ids."
                                                   f"Actual number of product ids: {len(get_response['ids'])}")

        if product_type == "variable":
            assert get_response["attributes"], f"Error. Get variable product response returned empty list for 'attributes'."
            assert get_response["attributes"] == get_response["attributes"], (f"Create variable product post and get call 'attributes' field are not the same."
                                                                              f"POST: {post_response['attributes']}, GET: {get_response['attributes']} ")


        logger.info(f"Successfully found product with id: {product_id} via api GET call")

        # verify product is in the database
        db_product = self.products_dao.get_product_by_id(product_id)

        # DB assertions
        assert db_product, f"Create a {product_type} product POST api call not recorded in database."
        assert db_product[0]['post_name'] == product_name, (f"Create a {product_type} product has unexpected name in database."
                                                            f"Expected: {product_name}, Actual: {db_product[0]['post_name']}")
        logger.info(f"Successfully found product with id: {product_id} in DB")