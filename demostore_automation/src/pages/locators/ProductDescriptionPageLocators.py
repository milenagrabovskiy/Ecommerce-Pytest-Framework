
from selenium.webdriver.common.by import By

class ProductDescriptionPageLocators:

    PRODUCT_TITLE = (By.CSS_SELECTOR, "h1.product_title.entry-title")
    #PRODUCT_MAIN_IMAGE = (By.CSS_SELECTOR, 'img[src="http://dev.bootcamp.store.supersqa.com/wp-content/uploads/2024/10/hoodie-2.jpg"]')
    #PRODUCT_MAIN_IMAGE = (By.CLASS_NAME, 'zoomImg')
    PRODUCT_MAIN_IMAGE = (By.CSS_SELECTOR, 'img.wp-post-image')
    #PRODUCT_MAIN_IMAGE = (By.XPATH, '//*[@id="product-20"]/div[1]/div/div/div[1]/img')
    PRODUCT_ALTERNATE_IMAGES = (By.CSS_SELECTOR, 'ol.flex-control-nav.flex-control-thumbs li img')
