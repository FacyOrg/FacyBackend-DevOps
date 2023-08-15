from flask import Flask, request
import cv2
import redis
import uuid
import base64
import json
import numpy as np
from deepface import DeepFace

app = Flask(__name__)

# redis_host = 'localhost'
# redis_port = 6379
# redis_db = 0
# redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

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

@app.route("/ai-img/run_task", methods=["POST"])
def analyze_and_store_image():
    data = request.json
    str_image = data["image"]

    decoded_image = base64.b64decode(str_image)
    nparr = np.frombuffer(decoded_image, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    result = DeepFace.analyze(img, actions=['emotion', 'age', 'gender', 'race'])
 
    instance_id = str(uuid.uuid4())
    
    # redis_key = f'image_analysis:{instance_id}'
    # redis_client.hmset(redis_key, result)
    
    # print(f"Image analysis for {image_path} saved with instance ID: {instance_id}\n")
    # print(result)
    rdata = get_rdata(result[0])
    
    return rdata
    

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
