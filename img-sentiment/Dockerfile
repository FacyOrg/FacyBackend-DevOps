FROM python:3.10
RUN apt update -y
RUN pip install redis pika numpy opencv-python-headless deepface
RUN apt install libgl1-mesa-glx -y
COPY worker_img_sentiment_analysis.py /app/worker_img_sentiment_analysis.py

WORKDIR /app

CMD ["python3.10", "worker_img_sentiment_analysis.py"]