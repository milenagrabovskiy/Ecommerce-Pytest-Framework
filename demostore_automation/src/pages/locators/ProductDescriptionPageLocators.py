
from selenium.webdriver.common.by import By

class ProductDescriptionPageLocators:

    PRODUCT_TITLE = (By.CSS_SELECTOR, "h1.product_title.entry-title")
    PRODUCT_MAIN_IMAGE = (By.CSS_SELECTOR, 'img.wp-post-image')
    PRODUCT_ALTERNATE_IMAGES = (By.CSS_SELECTOR, 'ol.flex-control-nav.flex-control-thumbs li img')
    REVIEWS_LINK = (By.CSS_SELECTOR, 'a[href="#tab-reviews"]')
    PRODUCT_REVIEW_STARS = (By.CSS_SELECTOR, 'div.comment-form-rating p.stars a.star-5')
    REVIEW_FIELD = (By.ID, 'comment')
    REVIEW_NAME_FIELD = (By.ID, 'author')
    REVIEW_EMAIL_FIELD = (By.ID, 'email')
    SUBMIT_BTN = (By.ID, 'submit')
    SUCCESS_MSG = (By.CSS_SELECTOR, 'em.woocommerce-review__awaiting-approval')
