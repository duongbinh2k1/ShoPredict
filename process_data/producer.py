import pika
from process_data.mongo_db import MongoDBClient
from datetime import datetime, time
import json


def publish_product_to_queue(start_time=datetime.combine(datetime.now(), time.min), end_time=datetime.combine(datetime.now(), time.max), offset=0, limit=20):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    database_url = "mongodb://localhost:27017/"
    database_name = "shopredict"
    collection_name = "products"

    mongo_client = MongoDBClient(database_url, database_name)

    query = {
        'get_at': {
            '$gte': start_time,
            '$lt': end_time
        }
    }

    while True:
        results = mongo_client.get_page(
            collection_name=collection_name, query=query, offset=offset, limit=limit)
        for result in results:
            result["_id"] = str(result["_id"])
            result['get_at'] = result['get_at'].isoformat()
            product_data = json.dumps(result)
            print(f"Publishing product data: {product_data}")
            channel.basic_publish(
                exchange='', routing_key='image_queue', body=product_data)

        if not results:
            channel.basic_publish(exchange='', routing_key='image_queue', body='finish')
            break
        else:
            offset += limit

    mongo_client.close_connection()
    connection.close()
