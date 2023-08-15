from flask import Flask, request
import cv2
import redis
import uuid
import os
import base64
import json
import numpy as np
from deepface import DeepFace
import pika

app = Flask(__name__)

redis_host = os.environ["REDIS_SVC"]
redis_port = 6379
redis_db = 1
r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

# Set up RabbitMQ connection
rabbitmq_host = os.environ["RABBITMQ_HOST"]
rabbitmq_user = 'admin'
rabbitmq_password = 'admin'
rabbitmq_virtual_host = '/'  # Default virtual host
# rabbitmq_port = os.environ["RABBITMQ_PORT"]

credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
rabbitmq_parameters = pika.ConnectionParameters(
    host=rabbitmq_host,
    port=5672,
    virtual_host=rabbitmq_virtual_host,
    credentials=credentials
)
connection = pika.BlockingConnection(rabbitmq_parameters)
channel = connection.channel()

# Declare the same queue as the producer
channel.queue_declare(queue='image_analysis_tasks')

def get_rdata(data):
    rdata = {
        "angry":data["emotion"]["angry"],
        "disgust":data["emotion"]["disgust"],
        "fear":data["emotion"]["fear"],
        "happy":data["emotion"]["happy"],
        "sad":data["emotion"]["sad"],
        "surprise":data["emotion"]["surprise"],
        "neutral":data["emotion"]["neutral"],
        "age":data["age"]
    }
    
    return rdata

def process_image(image):
    decoded_image = base64.b64decode(image)
    nparr = np.frombuffer(decoded_image, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    result = DeepFace.analyze(img, actions=['emotion', 'age'])
 
    rdata = get_rdata(result[0])
    
    return rdata
    
def callback(ch, method, properties, body):
    print(f" [x] Received image - work in progress...")
    body_str = body.decode('utf-8')
    body_dict = json.loads(body_str)

    task_id = body_dict["image_request_id"]

    r.hset("AI_IMG_WORKERS", str(task_id), json.dumps({"status":False}))

    result = process_image(body_dict["image"])
    
    r.hset("AI_IMG_WORKER", str(task_id), json.dumps({
        "status":True,
        "data": result
    }))
    print(f" [x] Done processing the image")
    
    # ch.basic_ack(delivery_tag = method.delivery_tag)
    

channel.basic_consume(queue='image_analysis_tasks',
                      on_message_callback=callback,
                      auto_ack=True)

# Start consuming messages
print('Worker is waiting for tasks. To exit press CTRL+C')
channel.start_consuming()
