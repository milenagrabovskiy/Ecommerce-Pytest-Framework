"""Tests for WooCommerce product creation with regular and sale prices.

Includes tests for:
  - Invalid sale prices (greater than or equal to regular price or non-numeric)
  - Boundary sale prices (just below regular price, very large/small values)

Uses the `setup_teardown` fixture for API helpers, database verification, and cleanup.
"""
import pytest
import logging as logger
from demostore_automation.tests.backend.products.test_create_products_smoke import setup_teardown

pytestmark = [pytest.mark.products, pytest.mark.create_product]

@pytest.mark.invalid_sale_price
@pytest.mark.parametrize(
    "regular_price, sale_price",
    [
        pytest.param("5.00", "10.00", marks=[pytest.mark.ebe28], id="sale_price > regular_price"),
        pytest.param("10.00", "10.00", marks=[pytest.mark.ebe29], id="sale_price == regular_price"),
        pytest.param("9999999.99", "9999999.99", marks=[pytest.mark.ebe30], id="very large sale_price == regular_price"),
        pytest.param("0.00", "9999999.99", marks=[pytest.mark.ebe31], id="very large sale_price > regular_price"),
        pytest.param("10.00", "abc", marks=[pytest.mark.ebe32], id="letter string sale_price"),
    ]
)


def test_invalid_sales_price(setup_teardown, regular_price, sale_price):
    """Test that creating a product with sale_price greater than or equal to regular_price
    results in the API ignoring the sale_price and setting it to an empty string.

    Args:
        setup_teardown (fixture): Fixture providing API helpers.
        regular_price (str): Regular price of the product.
        sale_price (str): Sale price of the product.

    Raises:
        AssertionError: If the API or DB does not handle invalid sale_price correctly.
    """
    # create payload with sale_price and regular_price
    payload = {
        "regular_price" : regular_price,
        "sale_price": sale_price
    }

    # create product with payload
    post_response = setup_teardown['products_api_helper'].call_create_product(payload)
    product_id = post_response['id']
    setup_teardown['product_ids'].append(product_id)
    logger.info(f"POST response for sale_price > regular_price create product test: {post_response}")

    # make GET call to make sure api ignores sale_price and sets it to an empty string.
    get_response = setup_teardown['generic_products_helper'].verify_product_is_created(post_response)
    assert get_response, "Product with invalid sale_price test not found in api and/or db"

    # verify sale_price and 'regular_price' are correct
    logger.info(f"GET response for sale_price > regular_price create product test: {get_response}")

    assert get_response['sale_price'] == '', (f"GET response for create product with invalid sale_price test"
                              f"did not ignore invalid sale_price. Actual: {get_response['sale_price']}. Expected: ''")
    assert get_response['regular_price'] == regular_price, (f"GET response for create product with invalid sale_price test"
                                                            f"create product test returned unexpected 'regular_price'."
                                                            f"Actual: {get_response['regular_price']}, Expected: {regular_price}")



@pytest.mark.sale_price_edge
@pytest.mark.parametrize(
    "regular_price, sale_price",
    [
        pytest.param("10.00", "9.99", marks=[pytest.mark.ebe33], id="sale price one cent off of regular"),
        pytest.param("9999999.99", "9999999.90", marks=[pytest.mark.ebe34], id="very large price and sale price"),
        pytest.param("10.00", "0.01", marks=[pytest.mark.ebe35], id="sale price=0.01"),
        pytest.param("10.00", "0.00000001", marks=[pytest.mark.ebe36], id="very small sale price"),
    ]
)

def test_price_boundaries(setup_teardown, regular_price, sale_price):
    """Test creating a product with valid sale_price within acceptable boundaries.

    This test verifies that when a product is created with a sale_price that is
    less than the regular_price, the API stores the correct values for both
    regular_price and sale_price, and the product is properly recorded in the DB.

    Args:
        setup_teardown (fixture): Fixture providing API and database helpers.
        regular_price (str): Regular price to use when creating the product.
        sale_price (str): Sale price to use when creating the product.

    Raises:
        AssertionError: If the API or database does not store prices correctly.
    """
    # create payload with sale_price and regular_price
    payload = {
        "regular_price" : regular_price,
        "sale_price": sale_price
    }

    # create product with payload
    post_response = setup_teardown['products_api_helper'].call_create_product(payload)
    product_id = post_response['id']
    setup_teardown['product_ids'].append(product_id)
    logger.info(f"POST response for sale_price > regular_price create product test: {post_response}")

    # make GET call to make sure product in db and api.
    get_response = setup_teardown['generic_products_helper'].verify_product_is_created(post_response)
    assert get_response, "Product with valid sale_price test not found in api and/or db"

    # verify 'sale_price' and 'regular_price' are correct
    logger.info(f"GET api response for newly created product with id {product_id}: {get_response}")

    assert get_response['sale_price'] == post_response['sale_price'], (f"GET response for create product with valid sale_price test"
                              f"ignored valid sale_price. Actual: {get_response['sale_price']}. Expected: {post_response['sale_price']}")
    assert get_response['regular_price'] == regular_price, (f"GET response for create product with valid sale_price test"
                                                            f"create product test returned unexpected 'regular_price'."
                                                            f"Actual: {get_response['regular_price']}, Expected: {post_response['regular_price']}")
