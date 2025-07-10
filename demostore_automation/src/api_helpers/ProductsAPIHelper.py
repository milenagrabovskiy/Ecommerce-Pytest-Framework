
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

            if len(api_response) < per_page:
                break

            page += 1
            
        return all_products

        