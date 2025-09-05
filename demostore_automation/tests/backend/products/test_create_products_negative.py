"""Negative tests for WooCommerce product creation.

Includes parameterized tests for invalid product fields (type, SKU, regular_price, stock_quantity)
and a test for creating a product with an empty payload, verifying defaults and existence in API and DB.
"""
import pytest
import logging as logger
from demostore_automation.tests.backend.products.test_create_products_smoke import setup_teardown

pytestmark = [pytest.mark.products, pytest.mark.create_product]

@pytest.mark.create_product_neg
@pytest.mark.parametrize(
    "param, value",
    [
        pytest.param("type", "invalid_type", marks=[pytest.mark.ebe37], id="invalid product type:str"),
        pytest.param("type", 123, marks=[pytest.mark.ebe38], id="invalid product type:int"),
        pytest.param("sku", "invalid_sku", marks=[pytest.mark.ebe39], id="invalid product sku:str"),
        pytest.param("sku", 123, marks=[pytest.mark.ebe40], id="invalid product sku:int"),
        pytest.param("regular_price", 10.00, marks=[pytest.mark.ebe41], id="invalid regular_price:float"),
        pytest.param("regular_price", 10, marks=[pytest.mark.ebe42], id="invalid regular_price:int"),
        pytest.param("stock_quantity", "abc", marks=[pytest.mark.ebe43], id="invalid stock_quantity: rand str"),
        pytest.param(
            "regular_price", "-10.00",
            marks=[
                pytest.mark.ebe45,
                pytest.mark.xfail(
                    reason="woocommerce bug: accepts negative regular_price as valid. negative float in DB, but FE shows '0.00'")
            ],
            id="invalid regular_price:negative"
        ),
        pytest.param(
            "regular_price", "abc",
            marks=[
                pytest.mark.ebe46,
                pytest.mark.xfail(
                    reason="woocommerce bug: accepts letters in string, but 'stock_quantity' throws an error. Returns 'False' for 'purchasable'"
                )
            ],
            id="invalid regular_price: random string"
        ),
    ]
)

def test_create_product_invalid_param(setup_teardown, param, value):
    """Test product creation with invalid parameters.

    Sends a create product request with invalid parameter values and
    verifies that the WooCommerce API returns an appropriate error.

    Args:
        setup_teardown (dict): Fixture providing helpers for API and DB access.
        param (str): The product parameter being tested (e.g., "type", "sku").
        value (any): The invalid value to send for the parameter.
    """
    # create product with invalid param and assert correct error message is displayed
    post_response = setup_teardown['generic_products_helper'].create_product_invalid_param(param, value)
    setup_teardown['generic_products_helper'].verify_error_message(post_response, param)
    logger.info(f"Post response for param: {param} is: {post_response}")

@pytest.mark.ebe44
def test_create_empty_product_neg(setup_teardown):
    """Test creating a product with an empty payload.

    Verifies that WooCommerce creates a product with default values when
    no fields are provided. Also checks that the product exists in the API
    and the database.

    Args:
        setup_teardown (dict): Fixture providing helpers for API and DB access.
    """
    response = setup_teardown['products_api_helper'].call_create_product(payload={})
    assert response, ("Create product with empty payload returned empty response. Woocommerce api has no mandatory fields for creating a product."
                      "Expected status code: 201")
    prod_id = response['id']
    setup_teardown['product_ids'].append(prod_id) # for teardown

    # assert default values are assigned to product
    assert response["type"] == "simple", (f"Create product with empty payload returned wrong product type."
                                          f"Default product type: 'simple'. Actual: {response['type']} ")
    assert response["name"] == "Product", (f"Create product with empty payload returned wrong product name."
                                          f"Default product name: 'Product'. Actual: {response['name']} ")

    # verify product exists via api and in db
    setup_teardown['generic_products_helper'].verify_product_is_created(response)