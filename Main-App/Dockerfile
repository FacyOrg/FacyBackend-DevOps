FROM python:3.10

RUN apt update 
RUN pip install --upgrade pip 
RUN pip3 install requests jwt redis uuid opencv-python flask
WORKDIR /App

COPY . .

CMD ["python3.10", "app.py"]



