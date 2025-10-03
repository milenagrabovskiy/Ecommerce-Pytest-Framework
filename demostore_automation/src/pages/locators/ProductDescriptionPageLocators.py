
from selenium.webdriver.common.by import By

class ProductDescriptionPageLocators:

    PRODUCT_TITLE = (By.CSS_SELECTOR, "h1.product_title.entry-title")
    PRODUCT_MAIN_IMAGE = (By.CSS_SELECTOR, 'img.wp-post-image')
    PRODUCT_ALTERNATE_IMAGES = (By.CSS_SELECTOR, 'ol.flex-control-nav.flex-control-thumbs li img')
    ON_SALE = (By.CSS_SELECTOR, 'div.post-31 span.onsale')
    CROSSED_OUT_ORIG_PRICE = (By.CSS_SELECTOR, 'p.price del[aria-hidden="true"]')
    REVIEWS_LINK = (By.CSS_SELECTOR, 'a[href="#tab-reviews"]')
    PRODUCT_REVIEW_STARS = (By.CSS_SELECTOR, 'div.comment-form-rating p.stars a.star-5')
    REVIEW_FIELD = (By.ID, 'comment')
    REVIEW_NAME_FIELD = (By.ID, 'author')
    REVIEW_EMAIL_FIELD = (By.ID, 'email')
    SUBMIT_BTN = (By.ID, 'submit')
    SUCCESS_MSG = (By.CSS_SELECTOR, 'em.woocommerce-review__awaiting-approval')
    #DECREASE_PRODUCT_BTN = (By.CSS_SELECTOR, 'button.wc-block-components-quantity-selector__button.wc-block-components-quantity-selector__button--minus')
    #PRODUCT_QTY_FIELD = (By.ID, 'quantity_68cf0851d146d')
    #PRODUCT_QTY_FIELD = (By.XPATH, '//*[@id="quantity_68cf0f836b4c1"]')
    PRODUCT_QTY_FIELD = (By.CLASS_NAME, 'input-text')
    ADD_TO_CART = (By.CSS_SELECTOR, 'button.single_add_to_cart_button.button.alt')

    COLOR_DROPDOWN = (By.ID, 'pa_color')
    LOGO_DROPDOWN = (By.ID, 'logo')
    PRODUCT_SKU = (By.CSS_SELECTOR, 'div.product_meta span.sku_wrapper span.sku')
    CLEAR_OPTIONS = (By.CSS_SELECTOR, 'a.reset_variations')