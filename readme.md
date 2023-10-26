# Shopee Data Crawling and Clothing Classification Model Training Project

This project utilizes Apache Airflow to automatically crawl data from Shopee, save the CSV data file to Google Drive, clean the data, store it in MongoDB, train a clothing classification model based on images, and save the results in MongoDB. In addition, RabbitMQ is used to manage queues and transmit data from MongoDB to the model.

## Usage Guide

![Diagram](https://github.com/duongbinh2k1/ShoPredict/blob/master/diagram.png?raw=true)

### Requirements

- Python 3.10.x
- Docker
- Google Drive API Credentials

### Installation

1. Clone this repository to your computer.

2. Get the image dataset from [Kaggle](https://www.kaggle.com/datasets/agrigorev/clothing-dataset-full).

3. Train the model by running the file: `clothes-classifier-vgg16-body-frozen.ipynb`.

4. Obtain the `client_secrets.json` file for authenticating Google Drive via Google Console. You can follow the tutorial [here](https://pythonhosted.org/PyDrive/quickstart.html).

5. Run Docker Compose:
    ```bash
    docker-compose up airflow-init
    docker-compose up
    ```
   This will initialize Apache Airflow and run the project.
