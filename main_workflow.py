import os
from dotenv import load_dotenv
from Scripts.total_sales_pipeline import SalesPipeline
from Scripts.postgres_pipeline import PostgresPipeline


def get_credentials(env_file):
    load_dotenv(env_file)
    return os.getenv("db_name"), os.getenv("user"), os.getenv("password")


if __name__ == "__main__":
    main_path = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(main_path, "Input_files")
    queries_path = os.path.join(main_path, "Queries")

    env_file = os.path.join(input_path, ".env")
    creds_file = os.path.join(input_path, "credentials_HH.json")
        
    SP = SalesPipeline(creds_file)
    store_sales = SP.get_store_sales()
    digital_sales = SP.get_digital_sales()
    
    db_name, user, pswd = get_credentials(env_file)
    
    PP = PostgresPipeline(queries_path, user, pswd)
    PP.create_and_fill_tables(db_name, store_sales, digital_sales)    