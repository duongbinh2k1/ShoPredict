import pymongo

class MongoDBClient:
    def __init__(self, database_url, database_name):
        self.client = pymongo.MongoClient(database_url)
        self.db = self.client[database_name]

    def insert_many_df(self, collection_name, df):
        try:
            collection = self.db[collection_name]
            records = df.to_dict(orient='records')
            result = collection.insert_many(records)
            print('Insert data to mongo successfully')
        except Exception as e:
            print(f"Error: {e}")

    def close_connection(self):
        self.client.close()