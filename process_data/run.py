from process_data.mongo_db import MongoDBClient
from process_data.utils import clean_data
import os

def clean_and_store_data(file):
    database_url = "mongodb://localhost:27017/"
    database_name = "shopredict"
    collection_name = "products"
    mongo_client = MongoDBClient(database_url, database_name)
    
    df = clean_data(os.path.join('files', file))

    mongo_client.insert_many_df(collection_name, df)
    
    mongo_client.close_connection()

def delete_file(file):
    try:
        os.remove(os.path.join('files', file))
    except Exception as e:
        print(f'Error: {e}')