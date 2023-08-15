from flask import Flask, request, jsonify
import requests
import os
import jwt
import base64
import redis
import hashlib
import json
import uuid
import cv2
import numpy as np
from datetime import datetime
import pika

app = Flask(__name__)

redis_host = os.environ["REDIS_SVC"] 
r = redis.StrictRedis(host=redis_host, port=6379, decode_responses=True, db=1)

IMG_SENTIMENT_ANALYSIS_PATH = "http://" + os.environ["IMG_SENTIMENT_ANALYSIS"] + os.environ["IMG_SENTIMENT_ANALYSIS_PORT"] + "/ai-img/run_task"

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

def generate_unique_id():
    return str(uuid.uuid4())

# async def process_image(image):
#     image_request_id = generate_unique_id()

#     data = {
#         "image": image,
#         "image_request_id": image_request_id
#     }

#     res = requests.post(IMG_SENTIMENT_ANALYSIS_PATH, json=data)

#     return image_request_id, res.json()


@app.route("/api/sentiment_analysis_image", methods=["POST"])
async def sentiment_analysis_image():
    try:
        image = request.files["image"]
        image_data = base64.b64encode(image.read()).decode("utf-8")

        if not image:
            return "No image uploaded!", 400

        connection = pika.BlockingConnection(rabbitmq_parameters)
        channel = connection.channel()
        
        channel.queue_declare(queue='image_analysis_tasks')
        
        image_request_id = generate_unique_id()
        body_data = json.dumps({
            "image": image_data,
            "image_request_id": image_request_id
        })

        channel.basic_publish(exchange='',
                              routing_key='image_analysis_tasks',
                              body=body_data)
        print(f" [x] Sent image for processing...")
        connection.close()
        
        return jsonify({"task_id": image_request_id}), 200
    except:
        return "Error: Could not upload image and continue the process!\n", 500

@app.route("/api/get_data_from_image_process")
async def get_data_from_image_process():
    args = request.args
    print(r.hgetall("AI_IMG_WORKER"))
    if "task_id" not in args:
        return "Task id is missing!", 400
    
    result = r.hget("AI_IMG_WORKER", args.get("task_id"))
    
    if result is None:
        return "Task id is invalid! Please provide a valid one.", 400
    
    result = json.loads(result)
    return jsonify(result), 200

@app.route("/api/sentiment_analysis_text", methods=["POST"])
def sentiment_analysis_voice():
    pass
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)