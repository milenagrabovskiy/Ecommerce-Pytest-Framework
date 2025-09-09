"""Test module for creating and verifying WooCommerce product reviews.

This module covers API and DB verification for product reviews, including:
- Reviews by guest users
- Reviews by registered customers
- Boundary testing for ratings (0-5)
- Invalid rating handling (>5, expected to xfail) as woocommerce expects a max rating of 5

Tests are parametrized using pytest.
"""
import pytest
import logging as logger

from demostore_automation.src.api_helpers.CustomerAPIHelper import CustomerAPIHelper
from demostore_automation.src.generic_helpers.generic_orders_helper import GenericOrdersHelper
from demostore_automation.src.utilities.genericUtilities import generate_random_email_and_password
from demostore_automation.src.utilities.wooAPIUtility import WooAPIUtility
from demostore_automation.tests.backend.products.test_create_products_smoke import setup_teardown

@pytest.mark.review
@pytest.mark.parametrize(
     "rating, customer_bought",
    [
        pytest.param(0, False, marks=[pytest.mark.ebe62], id="review-lowest boundary"),
        pytest.param(5, False, marks=[pytest.mark.ebe63], id="review-highest boundary"),
        pytest.param(10, False, marks=[pytest.mark.ebe64, pytest.mark.xfail(
                                                              reason='rating of >5 is invalid. valid:0-5')],
                                                              id="review-out of range"),
        pytest.param(4, True, marks=[pytest.mark.ebe65], id="registered customer review"),

    ]
)
def test_create_product_review(setup_teardown, rating, customer_bought):
    """Test creation and verification of a product review.

    Steps:
    1. Create a simple product via API.
    2. Optionally create a registered customer and order if `customer_bought` is True.
    3. Create a product review with the given rating.
    4. Verify review exists and is correct via both API and database.

    Args:
        setup_teardown (fixture): Fixture providing product helpers, API helpers, and teardown logic.
        rating (int): Rating for the review (0-5 recommended).
        customer_bought (bool): Whether the review is by a registered customer.

    Assertions:
        - Review exists in API response with correct rating, status, and reviewer info.
        - Review exists in DB with correct customer_id (if registered), email, and approved status.
    """
    created_customers = []  # for teardown
    post_response = setup_teardown['generic_products_helper'].create_product_by_type('simple')

    logger.info(f"product: {post_response}")

    product_id = post_response['id']
    setup_teardown['product_ids'].append(product_id)
    if customer_bought:
        random_email = generate_random_email_and_password(email_prefix="test_user")["email"]
        password = "Password123abc!"
        payload = {
            "email": random_email,
            "password": password
            }
        create_cust = WooAPIUtility().post("customers", params=payload, expected_status_code=201)
        customer_id = create_cust['id']
        created_customers.append(customer_id)
        generic_orders_helper = GenericOrdersHelper()
        payload = {
            "customer_id": customer_id,
            "line_items": [{"product_id": product_id, "quantity": 1}],
            "status": "completed",
            "billing": {
                "first_name": "Test_f",
                "last_name": "Test_l",
                "email": random_email
            }
        }
        create_order_responses = generic_orders_helper.create_order(additional_args=payload)
        for create_order_response in create_order_responses:
            assert create_order_response, f"Create order as guest user API response is empty"

    if customer_bought:
        # create customer & order as before
        review_response = setup_teardown['generic_products_helper'].create_product_review(
            product_id,
            rating,
            reviewer="Test User",
            email=random_email  # registered customer's email
        )
    else:
        review_response = setup_teardown['generic_products_helper'].create_product_review(
            product_id,
            rating
        )
    logger.info(f"Review response: {review_response}")

    cust_id = customer_id if customer_bought else None
    email_to_pass = random_email if customer_bought else None

    setup_teardown['generic_products_helper'].verify_product_review_exists(product_id, rating, customer_bought,
                                                                           customer_id=cust_id,
                                                                           reviewer_email=email_to_pass
                                                                           )
    for customer_id in created_customers: # customer teardown
        try:
            CustomerAPIHelper().call_delete_customer(customer_id)
        except Exception as e:
            logger.error(f"Failed to delete customer with id {customer_id}. Error: {e}")
    logger.info(f"Successfully deleted customer(s) with id(s): {created_customers}")