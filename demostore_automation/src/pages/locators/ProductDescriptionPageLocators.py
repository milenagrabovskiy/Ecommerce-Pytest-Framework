
from selenium.webdriver.common.by import By

class ProductDescriptionPageLocators:

    PRODUCT_TITLE = (By.CSS_SELECTOR, "h1.product_title.entry-title")
    PRODUCT_MAIN_IMAGE = (By.CSS_SELECTOR, 'img.wp-post-image')
    PRODUCT_ALTERNATE_IMAGES = (By.CSS_SELECTOR, 'ol.flex-control-nav.flex-control-thumbs li img')
    ON_SALE = (By.CSS_SELECTOR, 'div.post-31 span.onsale')
    CROSSED_OUT_ORIG_PRICE = (By.CSS_SELECTOR, 'p.price del[aria-hidden="true"]')