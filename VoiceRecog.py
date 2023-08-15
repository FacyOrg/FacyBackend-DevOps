import torch
import torchaudio
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import pyttsx3
import speech_recognition as sr

model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
engine = pyttsx3.init()

def preprocess_audio(audio_path, sample_rate=16000, duration=5):
    waveform, _ = torchaudio.load(audio_path, num_frames=sample_rate * duration)
    return waveform

def extract_audio_features(waveform):
    return waveform

def predict_sentiment(audio_features):
    inputs = tokenizer(audio_features, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)
    predicted_sentiment = torch.argmax(probabilities, dim=1).item()
    return predicted_sentiment, probabilities.tolist()[0]

def main():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        audio_features = extract_audio_features(audio)
        sentiment_label, sentiment_probabilities = predict_sentiment(audio_features)
        
        sentiment_classes = ["Very Negative", "Negative", "Neutral", "Positive", "Very Positive"]
        predicted_sentiment_label = sentiment_classes[sentiment_label]
        
        response_message = f"The sentiment of your speech is predicted as: {predicted_sentiment_label}"
        engine.say(response_message)
        engine.runAndWait()

    except Exception as e:
        return "None"

if __name__ == "__main__":
    main()
