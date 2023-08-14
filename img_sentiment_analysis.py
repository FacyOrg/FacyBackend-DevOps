import cv2
import redis
import uuid
from deepface import DeepFace

# redis_host = 'localhost'
# redis_port = 6379
# redis_db = 0
# redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

def analyze_and_store_image(image_path):
 
    image = cv2.imread(image_path)
        
    result = DeepFace.analyze(image, actions=['emotion', 'age', 'gender', 'race'])
    
 
    instance_id = str(uuid.uuid4())
    

    # redis_key = f'image_analysis:{instance_id}'
    # redis_client.hmset(redis_key, result)
    
    print(f"Image analysis for {image_path} saved with instance ID: {instance_id}\n")
    print(result)
if __name__ == "__main__":
    image_paths = ['/home/kubernetes/FacyBackend-DevOps/test.jpg']  
    
    for image_path in image_paths:
        analyze_and_store_image(image_path)
