from flask import Flask, request
import requests
import os
import jwt
import base64
import redis
import hashlib
import json
import uuid
from datetime import datetime

app = Flask(__name__)
r = redis.StrictRedis(host="localhost", port=6379, decode_responses=True, db=1)

IMG_SENTIMENT_ANALYSIS_PATH = "http://" + os.environ["IMG_SENTIMENT_ANALYSIS"] + "/run_task"

def generate_unique_id():
    return str(uuid.uuid4())

async def send_img_data_to_process(image):
    image_request_id = generate_unique_id()
    
    data = {
        "image": image,
        "image_request_id": image_request_id
    }

    res = requests.post(IMG_SENTIMENT_ANALYSIS_PATH, json=data)

    return image_request_id, res

async def get_data_from_image_process(image_request_id):
    ## Obtain data somehow - TODO
    ## Return data in a a dict
    pass

@app.route("/sentiment_analysis_image", methods=["POST"])
async def sentiment_analysis_image():
    try:
        image = request.json["image"]
        img_bytes = base64.b64decode(image.encode('utf-8'))
        
        if not image:
            return "No image uploaded!", 400

        image_request_id, _ = await send_img_data_to_process(img_bytes)
        data = await get_data_from_image_process(image_request_id)
        
    except:
        return "Error: Could not upload image and continue the process!", 500

@app.route("/sentiment_analysis_text", methods=["POST"])
def sentiment_analysis_image():
    pass
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)