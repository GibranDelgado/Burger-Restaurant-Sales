import os
import psycopg2
from psycopg2 import sql, extras


class PostgresPipeline:
    def __init__(self, path, user, pswd):
        self.path = path
        self.user = user
        self.pswd = pswd
        self.conn_params = {
            "host": "localhost",
            "user": self.user,
            "password": self.pswd,
            "port": 5432,
        }
    
    def read_sql(self, file):
        with open(os.path.join(self.path, file), "r") as f:
            return f.read()
    
    def _create_connection(self, db_name, autocommit=False):
        conn = psycopg2.connect(dbname=db_name, **self.conn_params)
        conn.autocommit = autocommit
        return conn

    def create_and_fill_tables(self, db_name, store_sales, digital_sales):        
        #Admin connection
        conn_admin = self._create_connection(db_name="postgres", autocommit=True)
        cursor_admin = conn_admin.cursor()
        
        cursor_admin.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        if not cursor_admin.fetchone():
            cursor_admin.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
            )
            
        cursor_admin.close()
        conn_admin.close()


        #DB connection
        conn = self._create_connection(db_name=db_name)
        cursor = conn.cursor()
        
        cursor.execute(
            sql.SQL(self.read_sql("Create_store_sales_table.sql"))
            .format(table_name=sql.Identifier('storesales'))            
        )
        cursor.execute(
            sql.SQL(self.read_sql("Create_digital_sales_table.sql"))
            .format(table_name=sql.Identifier('digitalsales'))            
        )
        
        for table, df in [("storesales", store_sales), ("digitalsales", digital_sales)]:
            cursor.execute(
                sql.SQL("TRUNCATE TABLE {}").format(sql.Identifier(table))
            )
            
            insert_query = sql.SQL("INSERT INTO {} VALUES %s").format(
                sql.Identifier(table)
            )
            extras.execute_values(cursor, insert_query, df.values)
        

        cursor.execute(
            sql.SQL(self.read_sql("Create_total_sales_view.sql"))
            .format(view_name=sql.Identifier('totalsales'))            
        )

        conn.commit()
        cursor.close()
        conn.close()