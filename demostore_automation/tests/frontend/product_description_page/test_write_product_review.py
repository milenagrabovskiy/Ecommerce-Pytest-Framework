import pytest
from demostore_automation.src.pages.HomePage import HomePage
from demostore_automation.src.pages.MyAccountSignedOutPage import MyAccountSignedOutPage
from demostore_automation.src.pages.ProductDescriptionPage import ProductDescriptionPage
from demostore_automation.src.utilities.genericUtilities import (generate_random_string,
                                                                 generate_random_email_and_password)


pytestmark = [pytest.mark.reviews]

@pytest.mark.parametrize(
    "user_type",
    [
        pytest.param('guest_user'),
        pytest.param('registered_user')
    ]
)

@pytest.mark.usefixtures("init_driver", "setup")
class TestWriteProductReview:

    @pytest.fixture(scope="class")
    def setup(self, request):
        request.cls.home_page = HomePage(self.driver)
        request.cls.pdp = ProductDescriptionPage(self.driver)
        request.cls.my_acc_so = MyAccountSignedOutPage(self.driver)

        self.home_page.go_to_home_page()


    @pytest.mark.efe123
    def test_write_product_review(self, user_type):
        # create registered user
        if user_type == 'registered_user':  # create a registered user
            self.my_acc_so.go_to_my_account()
            self.registered_email = generate_random_email_and_password()['email']
            self.my_acc_so.input_register_email(self.registered_email)
            self.my_acc_so.input_register_password(generate_random_email_and_password()['password'])
            self.my_acc_so.click_register_button()

        #go to home page
        self.home_page.go_to_home_page()

        # click on product
        self.home_page.click_first_product()

        # go to reviews
        self.pdp.click_on_reviews_link()

        # select star rating
        self.pdp.click_on_stars_rating()

        # write review
        self.pdp.write_product_review(review_text='this is a review')

        if user_type == 'guest_user':
            # fill in reviewer name and email fields
            self.pdp.write_reviewer_name(name=generate_random_string())
            self.pdp.write_reviewer_email(email=generate_random_email_and_password()['email'])


        # submit and verify success
        self.pdp.click_submit_and_verify_success()