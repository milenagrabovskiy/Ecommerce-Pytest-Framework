
import os

class MainConfigs:

    @staticmethod
    def get_base_url():
        base_url = os.environ.get('BASE_URL')
        if not base_url:
            raise Exception("Environment variable 'BASE_URL' must be set.")
        else:
            return base_url

    @staticmethod
    def get_coupon_code(filter):

        if filter.upper() == 'FREE_COUPON':
            return "ssqa100"
        elif filter.upper() == '50_OFF':
            return "JFOADIUFHADF"
        else:
            raise Exception(f"Unknown value for parameter 'filter'. filter={filter}")

    @staticmethod
    def get_db_configs():

        DB_PORT = os.environ.get("DB_PORT")
        DB_HOST = os.environ.get("DB_HOST")
        DB_DATABASE = os.environ.get("DB_DATABASE")
        DB_TABLE_PREFIX = os.environ.get("DB_TABLE_PREFIX")

        db_configs = dict()

        if DB_PORT:
            db_configs['port'] = int(DB_PORT) 
        else:
            raise Exception("Environment variable 'DB_PORT' must be set.")
        
        if DB_HOST:
            db_configs['db_host'] = DB_HOST
        else:
            raise Exception("Environment variable 'DB_HOST' must be set.")
        
        if DB_DATABASE:
            db_configs['database'] = DB_DATABASE
        else:
            raise Exception("Environment variable 'DB_DATABASE' must be set.")
        
        if DB_TABLE_PREFIX:
            db_configs['table_prefix'] = DB_TABLE_PREFIX
        else:
            raise Exception("Environment variable 'DB_TABLE_PREFIX' must be set.")
        
        return db_configs
