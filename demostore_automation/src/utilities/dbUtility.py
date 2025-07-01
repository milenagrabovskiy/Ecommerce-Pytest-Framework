

import pymysql
import os
import logging as logger
from demostore_automation.src.utilities.credentialsUtility import CredentialsUtility
from demostore_automation.src.configs.MainConfigs import MainConfigs

class DBUtility(object):

    def __init__(self):
        creds_helper = CredentialsUtility()
        self.creds = creds_helper.get_db_credentials()

        self.db_configs = MainConfigs.get_db_configs()
        self.host = self.db_configs['db_host']
        self.port = self.db_configs['port']
        self.database = self.db_configs['database']
        self.table_prefix = self.db_configs['table_prefix']

    def create_connection(self):
        logger.info(f"Connecting to database: {self.host}")
        connection = pymysql.connect(host=self.host, user=self.creds['db_user'],
                                     password=self.creds['db_password'],
                                     port=self.port)
        return connection


    def execute_select(self, sql):

        conn = self.create_connection()

        try:
            logger.debug(f"Executing: {sql}")
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute(sql)
            rs_dict = cur.fetchall()
            cur.close()
        except Exception as e:
            raise Exception(f"Failed running sql: {sql} \n  Error: {str(e)}")
        finally:
            conn.close()

        return rs_dict


    def execute_sql(self, sql):
        pass