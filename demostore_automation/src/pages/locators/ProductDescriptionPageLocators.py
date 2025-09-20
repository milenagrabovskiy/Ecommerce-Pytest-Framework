
from selenium.webdriver.common.by import By

class ProductDescriptionPageLocators:

    PRODUCT_TITLE = (By.CSS_SELECTOR, "h1.product_title.entry-title")
    PRODUCT_MAIN_IMAGE = (By.CSS_SELECTOR, 'img.wp-post-image')
    PRODUCT_ALTERNATE_IMAGES = (By.CSS_SELECTOR, 'ol.flex-control-nav.flex-control-thumbs li img')
    # DECREASE_PRODUCT_BTN = (By.CSS_SELECTOR, 'button.wc-block-components-quantity-selector__button.wc-block-components-quantity-selector__button--minus')
    #PRODUCT_QTY_FIELD = (By.ID, 'quantity_68cf0851d146d')
    #PRODUCT_QTY_FIELD = (By.XPATH, '//*[@id="quantity_68cf0f836b4c1"]')
    PRODUCT_QTY_FIELD = (By.CLASS_NAME, 'input-text')
    ADD_TO_CART = (By.CSS_SELECTOR, 'button.single_add_to_cart_button.button.alt')

