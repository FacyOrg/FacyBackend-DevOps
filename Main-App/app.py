from flask import Flask, request
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

app = Flask(__name__)
r = redis.StrictRedis(host="localhost", port=6379, decode_responses=True, db=1)

IMG_SENTIMENT_ANALYSIS_PATH = "http://" + os.environ["IMG_SENTIMENT_ANALYSIS"] + os.environ["IMG_SENTIMENT_ANALYSIS_PORT"] + "/ai/run_task"

def generate_unique_id():
    return str(uuid.uuid4())

async def process_image(image):
    image_request_id = generate_unique_id()

    data = {
        "image": image,
        "image_request_id": image_request_id
    }

    res = requests.post(IMG_SENTIMENT_ANALYSIS_PATH, json=data)

    return image_request_id, res.json()


@app.route("/sentiment_analysis_image", methods=["POST"])
async def sentiment_analysis_image():
    try:
        image = request.files["image"]
        image_data = base64.b64encode(image.read()).decode("utf-8")

        if not image:
            return "No image uploaded!", 400

        image_request_id, res = await process_image(image_data)
        return res, 200
    except:
        return "Error: Could not upload image and continue the process!\n", 500

@app.route("/sentiment_analysis_text", methods=["POST"])
def sentiment_analysis_voice():
    pass
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)