import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")

sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    sentiment_scores = sia.polarity_scores(text)
    compound_score = sentiment_scores["compound"]
    
    if compound_score >= 0.05:
        print(compound_score)
        return "Positive"
    elif compound_score <= -0.05:
        print(compound_score)
        return "Negative"
        
    else:
        print(compound_score)
        return "Neutral"
        
while True:
    text = input("Enter some text (or type 'exit' to quit): ")
    
    if text.lower() == "exit":
        break
    
    sentiment = analyze_sentiment(text)
    print(f"Sentiment: {sentiment}")
