"""Test suite for coupon creation for the Demostore WooCommerce website.

Contains tests for creating coupons with valid and invalid discount types.

Fixtures:
    setup_teardown: Provides CouponAPIHelper instance and handles coupon cleanup.

Attributes:
    pytestmark (list): Pytest markers applied to all tests in this module.
"""
import pytest
import logging as logger
from demostore_automation.src.utilities.genericUtilities import generate_random_string
from demostore_automation.src.api_helpers.CouponAPIHelper import CouponAPIHelper

pytestmark = [pytest.mark.coupon_api]

@pytest.fixture(scope="module")
def setup_teardown():
    """Initialize CouponAPIHelper and provide it to tests.

    Yields:
        dict: A dictionary containing the CouponAPIHelper instance under
            the key 'coupon_api_helper' and 'coupon_ids'

    Cleanup:
        Deletes any coupons created during the tests by deleting coupon IDs
        collected in the 'coupon_ids' list.
    """

    coupon_api_helper = CouponAPIHelper()
    coupon_ids = [] # collects coupon ids for teardown

    info = {
        "coupon_api_helper": coupon_api_helper,
        "coupon_ids": coupon_ids
    }

    yield info

    deleted = []
    for coupon_id in coupon_ids:
        try:
            coupon_api_helper.call_delete_coupon(coupon_id)
            deleted.append(coupon_id)

        except Exception as e:
            logger.warning(f"ERROR: {e}. Unable to delete coupon id: {coupon_id}")

    logger.info(f"Deleted coupon ids: {deleted}")


@pytest.mark.parametrize(
    "discount_type",
    [
        pytest.param("percent", marks=[pytest.mark.ecom260]),
        pytest.param("fixed_cart", marks=[pytest.mark.ecom261]),
        pytest.param("fixed_product", marks=[pytest.mark.ecom262]),
        pytest.param(None, marks=[pytest.mark.ecom263])
    ]
)
def test_create_coupon_with_discount_type(setup_teardown, discount_type):
    """Test creating a coupon with various valid discount types.

    Verifies that the POST API creates the coupon correctly and the GET API
    retrieves the coupon with the expected values.

    Args:
        setup_teardown (dict): Fixture providing CouponAPIHelper instance and coupon IDs list.
        discount_type (str or None): Discount type to test; defaults to 'fixed_cart' if None.

    Raises:
        AssertionError: If the POST or GET API responses do not match expected values.
    """
    logger.info(f"Running test: 'test_create_coupon_with_valid_discount_types' for '{discount_type}'")

    coupon_api_helper = setup_teardown["coupon_api_helper"]
    coupon_code = generate_random_string("automation")
    amount = "100.00"
    expected_discount_type = discount_type if discount_type else "fixed_cart"

    payload = dict()
    payload["code"] = coupon_code
    payload["amount"] = amount
    if discount_type:
        payload["discount_type"] = discount_type

    # make POST api call
    post_response = coupon_api_helper.call_create_coupon(payload)

    # POST api assertions
    assert post_response['id'], "Create coupon POST API response missing ID."

    assert post_response['code'] == coupon_code, (f"Create coupon POST API response 'code' does not match expected."
                                             f"Expected: {coupon_code}, Actual: {post_response['code']}")

    assert post_response['amount'] == amount, (f"Create coupon POST API response 'amount' does not match expected."
                                          f"Expected: {amount}, Actual: {post_response['amount']}")

    assert post_response['discount_type'] == expected_discount_type, (f"Create coupon POST API response 'discount_type'"
                                                                 f"does not match expected."
                                                                 f"Expected: {expected_discount_type}, Actual: {post_response['discount_type']}")

    # make GET api call
    coupon_id = post_response["id"]
    get_response = coupon_api_helper.call_retrieve_coupon(coupon_id)

    # make GET api assertions
    assert get_response['id'], "Create coupon POST API response missing ID."

    assert get_response['code'] == coupon_code, (f"Create coupon POST API response 'code' does not match expected."
                                                  f"Expected: {coupon_code}, Actual: {get_response['code']}")

    assert get_response['amount'] == amount, (f"Create coupon POST API response 'amount' does not match expected."
                                               f"Expected: {amount}, Actual: {get_response['amount']}")

    assert get_response['discount_type'] == expected_discount_type, (f"Create coupon POST API response 'discount_type'"
                                                                      f"does not match expected."
                                                                      f"Expected: {expected_discount_type}, Actual: {get_response['discount_type']}")
    setup_teardown["coupon_ids"].append(coupon_id)


@pytest.mark.ecom264
def test_create_coupon_invalid_discount_type(setup_teardown):
    """Negative test: Verify invalid discount type returns an error.

    Args:
        setup_teardown (dict): Fixture providing CouponAPIHelper instance.

    Raises:
        AssertionError: If the API response does not match the expected error response.
    """
    logger.info("Running test: 'test_create_coupon_invalid_discount_type'")
    # need to generate random coupon code each time or api call will fail
    coupon_api_helper = setup_teardown["coupon_api_helper"]
    coupon_code = generate_random_string()
    amount = "50.00"
    discount_type = "free_cart" # invalid option hardcoded for negative test
    payload = {
        "code": coupon_code,
        "amount": amount,
        "discount_type": discount_type
    }
    # make api call
    response = coupon_api_helper.call_create_coupon(payload, expected_status_code=400)

    expected_failure_response = {'code': 'rest_invalid_param',
 'data': {'details': {'discount_type': {'code': 'rest_not_in_enum',
                                        'data': None,
                                        'message': 'discount_type is not one '
                                                   'of percent, fixed_cart, '
                                                   'and fixed_product.'}},
          'params': {'discount_type': 'discount_type is not one of percent, '
                                      'fixed_cart, and fixed_product.'},
          'status': 400},
 'message': 'Invalid parameter(s): discount_type'}

    # POST api assertion
    assert response == expected_failure_response, (f"Create coupon with invalid discount_type returned unexpected response."
                                                   f"Expected: {expected_failure_response}, Actual: {response}")

    # GET api assertion not needed as coupon should not exist for negative test case
