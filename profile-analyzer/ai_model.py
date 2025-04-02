from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import Textblob
def analyze_profile(text):
    vectorize=TfidfVectorizer(stop_words='english') #remove english stopword
    tfidf_matrix = vectorize.fit_transform([text])
    feature=vectorize.get_feature_names_out()
    sentiment_score=Textblob(text).sentiment.polarity
    return{
        "tfidf_feature":feature.tolist(),
         "sentiment_score":sentiment_score
    }
