import json
import random
import time

import pika
from pymongo import MongoClient

# db_host = '0.0.0.0'
db_host = 'mongo'

mongo_client = MongoClient(host=db_host)
db = mongo_client['fms']

# mq_host = '0.0.0.0'
mq_host = 'rabbitmq'
url = f'amqp://guest:guest@{mq_host}:5672/%2f'
parameters = pika.URLParameters(url)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

try:
    while True:
        cars = list(db['cars'].find())
        for car in cars:
            channel.basic_publish(
                '',
                'tracking',
                json.dumps({
                    "car_id": car["car_id"],
                    "speed": str(random.randint(0, 120))
                }),
                pika.BasicProperties(content_type='text/plain', delivery_mode=1)
            )
        time.sleep(10)
finally:
    connection.close()
