FROM python:3.10
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install libgl1-mesa-glx
RUN pip install --upgrade pip
RUN pip install flask redis opencv-python uuid tensorflow deepface

WORKDIR /sentimente
COPY . .
CMD ["python3.10","img_sentiment_analysis.py"]

