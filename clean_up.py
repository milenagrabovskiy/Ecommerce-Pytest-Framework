from demostore_automation.src.utilities.wooAPIUtility import WooAPIUtility
from demostore_automation.src.api_helpers.ProductsAPIHelper import ProductsAPIHelper
import logging as logger



woo_api = WooAPIUtility()
product_api_helper = ProductsAPIHelper()


def remove_products_without_image():
    all_products = product_api_helper.call_get_all_products()
    products_without_image = [item for item in all_products if not item.get("images")]

    total = len(products_without_image)
    print(f"Total products without images: {total}")

    for product in products_without_image:
        product_id = product["id"]
        logger.info(f"Deleting product with ID: {product_id}")

        woo_api.delete(f"products/{product_id}")

    updated_products = product_api_helper.call_get_all_products()
    logger.info(f"Successfully deleted products without an image."
                f"Number of all products left: {len(updated_products)}")






if __name__ == "__main__":
    remove_products_without_image()
