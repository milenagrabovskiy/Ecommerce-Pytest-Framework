from demostore_automation.src.utilities.dbUtility import DBUtility


class CouponsDAO():

    def __init__(self):
        self.db_helper = DBUtility()

#fetching coupon by coupon text or partial text

    def fetch_coupon_by_text(self, text):
        sql = f"""SELECT * FROM
        {self.db_helper.database}.{self.db_helper.table_prefix}posts
        WHERE
        post_type = 'shop_coupon'
        AND
        post_title = '{text}';"""
        rs_sql = self.db_helper.execute_select(sql)
        return rs_sql

    def fetch_coupon_by_discount_type(self, discount_type):
        sql = f"""SELECT * FROM demostore.wp_posts p
        JOIN demostore.wp_postmeta pm ON p.ID = pm.post_id
        WHERE p.post_type = 'shop_coupon'
        AND p.post_status = 'publish'
        AND pm.meta_key = 'discount_type'
        AND pm.meta_value = '{discount_type}';"""
        rs_sql = self.db_helper.execute_select(sql)
        return rs_sql
