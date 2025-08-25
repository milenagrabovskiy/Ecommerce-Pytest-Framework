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
