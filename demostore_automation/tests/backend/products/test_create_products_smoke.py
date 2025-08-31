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
from demostore_automation.src.generic_helpers.generic_products_helper import GenericProductsHelper
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
    generic_products_helper = GenericProductsHelper()
    product_ids = [] # collects product ids for teardown

    info = {
        "products_api_helper": products_api_helper,
        "products_dao": products_dao,
        "product_ids": product_ids,
        "generic_products_helper": generic_products_helper
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


@pytest.mark.parametrize(
    "product_type, additional_args",
    [
        pytest.param("simple", None, marks=[pytest.mark.ecom188, pytest.mark.create_products1], id="create_simple_product"),
        pytest.param("simple", {"virtual": True}, marks=[pytest.mark.ecom188, pytest.mark.create_products1], id="create_simple_virtual_product"),
        pytest.param("simple", {"downloadable": True}, marks=[pytest.mark.ecom188, pytest.mark.create_products1], id="create_simple_virtual_product"),
        pytest.param("simple", {"virtual": True,"downloadable": True}, marks=[pytest.mark.ecom188, pytest.mark.create_products1], id="create_simple_virtual_product"),
        pytest.param("grouped", None, marks=[pytest.mark.ecom188, pytest.mark.create_products2], id="create_grouped_product"),
        pytest.param("external", None, marks=[pytest.mark.ecom188, pytest.mark.create_products3], id="create_external_product"),
        pytest.param("variable", None, marks=[pytest.mark.ecom188, pytest.mark.create_products4], id="create_variable_product")
    ]
)
def test_create_product(setup_teardown, product_type, additional_args):
    # create product via api
    post_response = setup_teardown['generic_products_helper'].create_product_by_type(product_type)

    logger.info(f"product: {post_response}")

    product_id = post_response['id']
    setup_teardown['product_ids'].append(product_id) # for teardown

    # verify product exists in api and db
    assert setup_teardown['generic_products_helper'].verify_product_is_created(post_response)
