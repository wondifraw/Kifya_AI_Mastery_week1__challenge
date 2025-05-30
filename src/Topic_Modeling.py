import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import re
nltk.download('punkt')
nltk.download('stopwords')

class TopicModeling:
    def __init__(self, num_topics=5):
        self.num_topics = num_topics
        self.vectorizer = TfidfVectorizer()
        self.lda = LatentDirichletAllocation(n_components=self.num_topics, random_state=0)

    def preprocess_text(self, text):
        """Clean and tokenize the text."""
        stop_words = set(nltk.corpus.stopwords.words('english'))
        text = re.sub(r'\W+', ' ', text)
        tokens = nltk.word_tokenize(text.lower())
        tokens = [word for word in tokens if word not in stop_words]
        return ' '.join(tokens)

    def fit(self, dataframe, text_column):
        """Fit the LDA model on the cleaned text."""
        if text_column not in dataframe.columns:
            raise ValueError(f"The dataset must contain a '{text_column}' column.")
        
        dataframe['cleaned_text'] = dataframe[text_column].apply(self.preprocess_text)
        tfidf_matrix = self.vectorizer.fit_transform(dataframe['cleaned_text'])
        self.lda.fit(tfidf_matrix)
        return dataframe

    def display_topics(self):
        """Display the topics identified by LDA."""
        feature_names = self.vectorizer.get_feature_names_out()
        for idx, topic in enumerate(self.lda.components_):
            print(f"\nTopic {idx + 1}:")
            print(", ".join([feature_names[i] for i in topic.argsort()[-5:]]))