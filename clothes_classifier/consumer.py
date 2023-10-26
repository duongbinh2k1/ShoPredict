import pika
import torch
import requests
from PIL import Image
import torchvision.models as models
import torchvision.transforms as transforms
import io
import os
import pandas as pd

model = models.vgg16(pretrained=False)
# model_path = "./src/Vgg16_body_freezed_10_epochs.pth" 
model_path = os.path.join('clothes_classifier', 'src/Vgg16_body_freezed_10_epochs.pth')
# model.load_state_dict(torch.load(model_path))
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

    print(predicted_label)

    return predicted_label

def consume_image_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='image_queue')

    def callback(ch, method, properties, body):
        image_url = body.decode('utf-8')
        if image_url == 'finish':
            print('Received finish message. Stopping consumption.')
            channel.stop_consuming()
        else:
            # Process the image.
            type_clothes = predict_image(image_url=image_url, model=model)
            print(f"Processed image: {image_url}")

    channel.basic_consume(queue='image_queue', on_message_callback=callback, auto_ack=True)

    print('Start consuming')
    channel.start_consuming()

