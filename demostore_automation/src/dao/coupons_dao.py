from demostore_automation.src.utilities.dbUtility import DBUtility


class CouponsDAO():

    def __init__(self):
        self.db_helper = DBUtility()

#fetching coupon by coupon text or partial text

    def fetch_coupon_by_partial_string(self, partial_string):
        sql = f"""SELECT * FROM
        demostore.wp_posts
        WHERE
        post_type = 'shop_coupon'
        AND
        'post_name' = '{partial_string}';"""

        # def fetch_coupon_by_partial_string(self, partial_string):
        # sql = f"""SELECT * FROM
        # demostore.wp_posts
        # WHERE
        # post_type = 'shop_coupon'
        # AND
        # 'post_name' = 'ssqa100';"""