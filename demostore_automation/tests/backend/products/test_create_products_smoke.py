"""Test suite for creating WooCommerce products via API.

This module contains test cases that verifies product creation using the
WooCommerce REST API, and ensures the created product is persisted in both
the API and the database.

Fixtures:
    setup_teardown: Provides API and DAO helpers, handles test cleanup.

Tests:
    test_create_a_simple_product: Validates product creation and persistence.
"""

import pytest
import logging as logger
from demostore_automation.src.utilities.genericUtilities import generate_random_string
from demostore_automation.src.api_helpers.ProductsAPIHelper import ProductsAPIHelper
from demostore_automation.src.dao.products_dao import ProductsDAO

@pytest.fixture(scope="module")
def setup_teardown():
    """Setup and teardown fixture for product-related API tests.

    Initializes the ProductsAPIHelper and ProductsDAO instances.
    Collects created product IDs for cleanup after all tests in the module.

    Yields:
        dict: Dictionary containing:
            - 'products_api_helper' (ProductsAPIHelper): API utility for product endpoints.
            - 'products_dao' (ProductsDAO): DAO utility for querying product data from the database.
            - 'product_ids' (list): List to store IDs of products created during tests.

    Cleanup:
        Deletes all products listed in 'product_ids' via the API.
    """
    products_api_helper = ProductsAPIHelper()
    products_dao = ProductsDAO()
    product_ids = [] # collects product ids for teardown

    info = {
        "products_api_helper": products_api_helper,
        "products_dao": products_dao,
        "product_ids": product_ids
    }

    yield info

    deleted = []
    for product_id in product_ids:
        try:
            products_api_helper.call_delete_product(product_id)
            deleted.append(product_id)

        except Exception as e:
            logger.warning(f"ERROR: {e}. Unable to delete product with id: {product_id}")

    logger.info(f"Successfully deleted products with ids: {deleted}")


@pytest.mark.ecom188
def test_create_a_simple_product(setup_teardown):
    """Test creating a simple product via the WooCommerce API.

    Steps:
        - Create a product with 'simple' type and a random name.
        - Assert the POST response contains correct data.
        - Assert the product is retrievable via GET.
        - Assert the product exists in the database.
        - Track the product ID for teardown cleanup.

    Args:
        setup_teardown (dict): Fixture providing API helper, DAO helper, and product ID list.

    Raises:
        AssertionError: If any validation (API or DB) fails.
    """
    products_api_helper = setup_teardown['products_api_helper']
    logger.info("Running test: 'test_create_a_simple_product'")

    # create payload
    product_name = generate_random_string()
    product_type = "simple"
    regular_price = "21.99"
    payload = {
        "name": product_name,
        "type": product_type,
        "regular_price": regular_price
    }
    # make POST api call
    post_response = products_api_helper.call_create_product(payload=payload)
    product_id = post_response['id']
    # POST api call assertions
    assert post_response, "Create a simple product POST api call is empty."

    assert post_response['name'] == product_name, (f"Create a simple product POST api call response"
                                                   f"returned unexpected 'name'"
                                                   f"Expected: {product_name}, Actual: {post_response['name']}")

    assert post_response['type'] == product_type, (f"Create a simple product POST api call response"
                                                   f"returned unexpected 'product_type'"
                                                   f"Expected: {product_type}, Actual: {post_response['product_type']}")

    assert post_response['status'] == 'publish', (f"Create a simple product POST api call response"
                                                   f"returned unexpected 'status'"
                                                   f"Expected: 'publish', Actual: {post_response['status']}")

    # make GET api call to verify product exists
    get_response = products_api_helper.call_get_product_by_id(product_id)

    # POST api call assertions
    assert get_response, "Create a simple product GET api call is empty."

    assert get_response['name'] == product_name, (f"Create a simple product GET api call response"
                                                   f"returned unexpected 'name'"
                                                   f"Expected: {product_name}, Actual: {get_response['name']}")

    assert get_response['type'] == product_type, (f"Create a simple product GET api call response"
                                                   f"returned unexpected 'product_type'"
                                                   f"Expected: {product_type}, Actual: {get_response['product_type']}")

    # verify product is in the database
    products_dao = setup_teardown['products_dao']
    db_product = products_dao.get_product_by_id(product_id)

    # DB assertions
    assert db_product, "Create a simple product POST api call not recorded in database."
    assert db_product[0]['post_name'] == product_name, (f"Create a simple product has unexpected name in database."
                                                        f"Expected: {product_name}, Actual: {db_product[0]['post_name']}")

    # keep track of successfully created product ids by adding to list in fixture function
    setup_teardown['product_ids'].append(product_id)