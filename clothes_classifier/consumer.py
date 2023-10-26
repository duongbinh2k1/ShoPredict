import pika
import torch
import requests
from PIL import Image
import torchvision.models as models
import torchvision.transforms as transforms
import io
import os
import pandas as pd
import json
from process_data.mongo_db import MongoDBClient
import bson
from datetime import datetime

model = models.vgg16(pretrained=False)
model_path = os.path.join('clothes_classifier', 'src/Vgg16_body_freezed_10_epochs.pth')
model.load_state_dict(torch.load(model_path, map_location='cpu'))
model = model.cpu()
model.eval()

def predict_image(image_url, model=model):
    response = requests.get(image_url)
    image_data = response.content

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
    ])

    image = Image.open(io.BytesIO(image_data))
    image = transform(image)

    with torch.no_grad():
        output = model(image.unsqueeze(0))

    _, predicted_class = output.max(1)

    # print("Predicted class:", predicted_class.item())

    mapping_label = pd.read_csv(os.path.join('clothes_classifier', 'src/mapping_label.csv'))
    predicted_label = mapping_label[mapping_label['class_id'] == int(str(predicted_class.item())[0])]['class_label'].values[0]

    return predicted_label

def consume_product_queue(model=model):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='image_queue')

    def callback(ch, method, properties, body):
        data = body.decode('utf-8')
        if data == 'finish':
            print('Received finish message. Stopping consumption.')
            channel.stop_consuming()
        else:
            product_data = json.loads(data)

            if 'image' in product_data:
                image_url = product_data['image']

                type_clothes = predict_image(image_url=image_url, model=model)
                product_data['type'] = type_clothes

                database_url = "mongodb://localhost:27017/"
                database_name = "shopredict"
                collection_name = "classified_products"
                mongo_client = MongoDBClient(database_url, database_name)
                product_data['_id'] = bson.ObjectId(product_data['_id'] )
                product_data['get_at'] = datetime.fromisoformat(product_data['get_at'])
                mongo_client.insert_one(collection_name, product_data)

                print(f"Processed image: {image_url} and inserted into the database.")
            else:
                print("Invalid data format: missing 'image' field.")

    channel.basic_consume(queue='image_queue', on_message_callback=callback, auto_ack=True)

    print('Start consuming')
    channel.start_consuming()

