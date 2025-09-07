import pytest
import logging as logger

from demostore_automation.src.generic_helpers.generic_orders_helper import GenericOrdersHelper
from demostore_automation.src.utilities.genericUtilities import generate_random_email_and_password
from demostore_automation.src.utilities.wooAPIUtility import WooAPIUtility
from demostore_automation.tests.backend.products.test_create_products_smoke import setup_teardown

@pytest.mark.review
@pytest.mark.parametrize(
     "rating, customer_bought",
    [
        pytest.param(0, False, marks=[pytest.mark.a], id="review-lowest boundary"),
        pytest.param(5, False, marks=[pytest.mark.b], id="review-highest boundary"),
        pytest.param(10, False, marks=[pytest.mark.c, pytest.mark.xfail], id="review-out of range"),
        pytest.param(4, True, marks=[pytest.mark.c], id="registered customer review"),

    ]
)
def test_create_product_review(setup_teardown, rating, customer_bought):
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
        generic_orders_helper = GenericOrdersHelper()
        payload = {
            "customer_id": customer_id,
            "line_items": [{"product_id": product_id, "quantity": 1}],
            "status": "completed",
            "billing": {
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
            email=random_email  # <- must match the customer who bought
        )
    else:
        review_response = setup_teardown['generic_products_helper'].create_product_review(
            product_id,
            rating
        )
    logger.info(f"Review response: {review_response}")

    # verify review persisted via api and db
    reviews = setup_teardown['products_api_helper'].call_retrieve_reviews(product_id)
    if rating > 5:
        assert reviews[0]['rating'] == 5, f"Error. The maximum rating is 5. Rating in api: {reviews[0]['rating']}"
    logger.info(f"reviews: {reviews}")
    assert reviews, f"Get reviews response is empty after review for product id: {product_id}"
    assert 'test review' in reviews[0]['review']
    assert reviews[0]['status'] == "approved"
    if customer_bought:
        assert reviews[0]['verified']
    else:
        assert not reviews[0]['verified']