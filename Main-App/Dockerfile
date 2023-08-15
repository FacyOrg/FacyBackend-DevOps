FROM python:3.10
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install libgl1-mesa-glx
RUN pip install --upgrade pip 
RUN pip3 install requests jwt redis uuid opencv-python flask[async]
WORKDIR /App

COPY . .

CMD ["python3.10", "app.py"]



