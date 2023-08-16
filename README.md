# FacyBackend-DevOps

### This is Facy's API and infrastructure repository

It uses Minikube with kubectl for cluster. The API consists of a small Flask server that allows uploading an image with a person, for extracting its emotions and age. This is possible by using an API from DeepFace, which receives the image, processes it and returns the result. These events are happening inside RabbitMQ workers, allowing the API server to not be blocked by intensive operations. Data is stored and parsed between services through Redis, where the result and status of process are kept.
