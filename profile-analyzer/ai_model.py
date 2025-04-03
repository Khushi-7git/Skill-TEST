from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob

def analyze_profile(text):
    vectorizer = TfidfVectorizer(stop_words='english')  
    tfidf_matrix = vectorizer.fit_transform([text])
    features = vectorizer.get_feature_names_out().tolist()  
    sentiment_score = TextBlob(text).sentiment.polarity

    return {
        "tfidf_features": features,
        "sentiment_score": sentiment_score
    }
