import json

import pika
from pymongo import MongoClient

# db_host = '0.0.0.0'
db_host = 'mongo'

mongo_client = MongoClient(host=db_host)
db = mongo_client['fms']

# mq_host = '0.0.0.0'
mq_host = 'rabbitmq'
url = f'amqp://guest:guest@{mq_host}:5672/%2f'
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='tracking')


def callback(ch, method, properties, body):
    data = json.loads(body.decode())
    if 'car_id' in data and 'speed' in data:
        speed = int(data['speed'])
        if speed > 60:
            if speed <= 80:
                penalty = speed - 60
            elif speed <= 100:
                penalty = 2 * (speed - 80) + 20
            else:
                penalty = 5 * (speed - 100) + 40 + 20
            car = db['cars'].find_one(
                {"car_id": data["car_id"]}
            )
            if car:
                db['drivers'].update(
                    {'driver_id': car['driver_id']},
                    {'$inc': {'penalty': penalty}},
                    upsert=True
                )


channel.basic_consume('tracking', on_message_callback=callback)
channel.start_consuming()
connection.close()
