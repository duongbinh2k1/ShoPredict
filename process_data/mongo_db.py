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
    
    def get_page(self, collection_name, query=None, offset=0, limit=20):
        try:
            collection = self.db[collection_name]
            if query:
                result = collection.find(query).skip(offset).limit(limit)
            else:
                result = collection.find()
            data = list(result)
            return data
        except Exception as e:
            print(f"Error: {e}")
            return None

    def close_connection(self):
        self.client.close()