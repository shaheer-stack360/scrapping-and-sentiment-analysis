# import pandas as pd
# import nltk
# from nltk.sentiment import SentimentIntensityAnalyzer

# df = pd.read_csv("instagram_reviews.csv")
# #df.head()
# text = df['text']
# #print(text)
# tokens = nltk.word_tokenize(text[1])
# #print(tokens)

# labelled = nltk.pos_tag(tokens)
# print(labelled)

# sia = SentimentIntensityAnalyzer()

# print(sia.polarity_scores(text[0]))


import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
#import fasttext
#import os
#from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

df = pd.read_csv("instagram_reviews.csv")

rating_mapping = {
    1: "negative",
    2: "negative",
    3: "neutral",
    4: "positive",
    5: "positive"
}

df["rating"] = df["rating"].map(rating_mapping)
df = df.dropna(subset=["text", "rating"])

X = df["text"].astype(str)
y = df["rating"]

stop_words = set(stopwords.words("english")) - {"no", "not", "never", "nor", "neither", "without", "barely", "hardly", "scarcely"}

def preprocess(text):

    # Tokenization
    tokens = word_tokenize(text)

    # Stopword removal
    tokens = [
        word
        for word in tokens
        if word.lower() not in stop_words
    ]

    # POS tagging
    tagged_tokens = pos_tag(tokens)

    # Convert back to words for TF-IDF
    tokens = [word for word, tag in tagged_tokens]

    return " ".join(tokens)


X_processed = X.apply(preprocess)

vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    min_df=2,
    max_features=50000
)

X_features = vectorizer.fit_transform(X_processed)

X_train, X_test, y_train, y_test = train_test_split(
    X_features,
    y,
    test_size=0.2,
    random_state=42
)

classifier = LogisticRegression()

classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)


accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)

# def prepare_fasttext_data(X, y, filepath):
#     with open(filepath, "w", encoding="utf-8") as f:
#         for text, label in zip(X, y):
#             f.write(f"__label__{label} {text}\n")

# def train_fasttext(X_train, y_train, X_test, y_test):
#     train_file = "ft_train.txt"
#     test_file  = "ft_test.txt"
    
#     prepare_fasttext_data(X_train, y_train, train_file)
#     prepare_fasttext_data(X_test,  y_test,  test_file)
    
#     model = fasttext.train_supervised(
#         input=train_file,
#         epoch=25,
#         lr=0.5,
#         wordNgrams=2,
#         dim=100,
#     )
    
#     result = model.test(test_file)
#     print(f"FastText Accuracy: {result[1]:.4f}")
    
#     os.remove(train_file)
#     os.remove(test_file)

# def run_roberta(X_test, y_test):
#     sentiment_pipeline = pipeline(
#         "sentiment-analysis",
#         model="cardiffnlp/twitter-roberta-base-sentiment",
#         tokenizer="cardiffnlp/twitter-roberta-base-sentiment",
#         truncation=True,
#         max_length=512,
#     )

#     label_map = {
#         "LABEL_0": "negative",
#         "LABEL_1": "neutral",
#         "LABEL_2": "positive",
#     }

#     print("Running RoBERTa inference (this may take a few minutes)...")
#     predictions = []
#     for text in X_test:
#         result = sentiment_pipeline(text)[0]
#         predictions.append(label_map[result["label"]])

#     accuracy = accuracy_score(y_test, predictions)
#     print(f"RoBERTa Accuracy: {accuracy:.4f}")

# X_train_raw, X_test_raw, _, _ = train_test_split(
#     X_processed, y, test_size=0.2, random_state=42
# )
# train_fasttext(X_train_raw, y_train, X_test_raw, y_test)

# X_train_raw, X_test_raw, _, _ = train_test_split(
#     X, y, test_size=0.2, random_state=42
# )
# run_roberta(X_test_raw.tolist(), y_test.tolist())