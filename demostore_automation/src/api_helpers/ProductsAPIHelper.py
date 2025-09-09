
from demostore_automation.src.utilities.wooAPIUtility import WooAPIUtility


class ProductsAPIHelper:

    def __init__(self):
        self.woo_api_utility = WooAPIUtility()

    def call_get_product_by_id(self, product_id):
        return self.woo_api_utility.get(f"products/{product_id}", expected_status_code=200)
    
    def call_get_all_products(self, per_page=100):
        all_products = []
        page = 1

        while True:
            api_response = self.woo_api_utility.get("products", params={"page":page, "per_page":per_page}, expected_status_code=200)

            if not api_response:
                break 
            
            all_products.extend(api_response)

            # The last page is reached when there are less than 100 products per page. Break the loop.
            if len(api_response) < per_page:
                break

            page += 1
            
        return all_products


    def call_create_product(self, payload, expected_status_code=201):
        return self.woo_api_utility.post("products", params=payload, expected_status_code=expected_status_code)


    def call_delete_product(self, product_id):
        return self.woo_api_utility.delete(f"products/{product_id}")


    def call_create_review(self, payload, expected_status_code=201):
        return self.woo_api_utility.post("products/reviews", params=payload, expected_status_code=expected_status_code)


    def call_retrieve_reviews(self, product_id):
        return self.woo_api_utility.get("products/reviews", params={"product": product_id})