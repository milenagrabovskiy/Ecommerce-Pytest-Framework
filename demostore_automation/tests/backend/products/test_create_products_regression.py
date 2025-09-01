import pytest
import logging as logger
from demostore_automation.tests.backend.products.test_create_products_smoke import setup_teardown

@pytest.mark.invalid_sale_price
@pytest.mark.parametrize(
    "regular_price, sale_price",
    [
        pytest.param("5.00", "10.00", marks=[pytest.mark.invalid_sale_price1], id="sale_price > regular_price"),
        pytest.param("10.00", "10.00", marks=[pytest.mark.invalid_sale_price2], id="sale_price == regular_price"),
    ]
)


def test_sales_price_more_than_regular(setup_teardown, regular_price, sale_price):
    # create payload with sale_price < regular_price
    payload = {
        "regular_price" : regular_price,
        "sale_price": sale_price
    }

    # create product with payload
    post_response = setup_teardown['products_api_helper'].call_create_product(payload)
    product_id = post_response['id']
    logger.info(f"POST response for sale_price > regular_price create product test: {post_response}")

    # make GET call to make sure api ignores sale_price and sets it to an empty string.
    assert setup_teardown['generic_products_helper'].verify_product_is_created(post_response), f"Product with invalid sale_price test not found in api and/or db"

    get_response = setup_teardown['products_api_helper'].call_get_product_by_id(product_id)
    logger.info(f"GET response for sale_price > regular_price create product test: {get_response}")

    assert not get_response['sale_price'], (f"GET response for create product with invalid sale_price test"
                              f"did not ignore invalid sale_price. Actual: {get_response['sale_price']}. Expected: ''")
    assert get_response['regular_price'] == regular_price, (f"GET response for create product with invalid sale_price test"
                                                            f"create product test returned unexpected 'regular_price'."
                                                            f"Actual: {get_response['regular_price']}, Expected: {regular_price}")