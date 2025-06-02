import pandas as pd
import nltk
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim import corpora
from gensim.models import LdaModel

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


class HeadlineTopicModeler:
    """
    A class to perform topic modeling on news headlines using LDA and NLTK preprocessing.
    """

    def __init__(self, csv_path: str, headline_column: str):
        """
        Initializes the HeadlineTopicModeler.

        Parameters:
        - csv_path (str): Path to the CSV file containing headlines.
        - headline_column (str): The column name containing the headline text.
        """
        self.csv_path = csv_path
        self.headline_column = headline_column
        self.headlines = []
        self.cleaned_headlines = []
        self.dictionary = None
        self.corpus = None
        self.lda_model = None

    def load_data(self):
        """
        Loads the CSV file and extracts the headline column.
        """
        try:
            df = pd.read_csv(self.csv_path)
            if self.headline_column not in df.columns:
                raise ValueError(f"Column '{self.headline_column}' not found in CSV.")
            self.headlines = df[self.headline_column].dropna().astype(str).tolist()
            print(f"Loaded {len(self.headlines)} headlines.")
        except Exception as e:
            print(f"[ERROR] Could not load data: {e}")

    def preprocess_headlines(self):
        """
        Tokenizes, removes stopwords, and lemmatizes each headline.
        """
        try:
            stop_words = set(stopwords.words('english'))
            lemmatizer = WordNetLemmatizer()

            self.cleaned_headlines = []
            for headline in self.headlines:
                tokens = wordpunct_tokenize(headline.lower())
                filtered_tokens = [
                    lemmatizer.lemmatize(token)
                    for token in tokens if token.isalpha() and token not in stop_words
                ]
                self.cleaned_headlines.append(filtered_tokens)
            print("Preprocessing completed.")
        except Exception as e:
            print(f"[ERROR] Preprocessing failed: {e}")

    def build_lda_model(self, num_topics=5, passes=10):
        """
        Builds the LDA model on the preprocessed headlines.

        Parameters:
        - num_topics (int): Number of topics to discover.
        - passes (int): Number of passes through the corpus during training.
        """
        try:
            self.dictionary = corpora.Dictionary(self.cleaned_headlines)
            self.corpus = [self.dictionary.doc2bow(text) for text in self.cleaned_headlines]

            self.lda_model = LdaModel(
                corpus=self.corpus,
                id2word=self.dictionary,
                num_topics=num_topics,
                passes=passes,
                random_state=42
            )
            print("LDA model successfully built.")
        except Exception as e:
            print(f"[ERROR] Failed to build LDA model: {e}")

    def display_topics(self, num_words=5):
        """
        Displays the topics discovered by the LDA model.

        Parameters:
        - num_words (int): Number of top words to display per topic.
        """
        try:
            if not self.lda_model:
                raise ValueError("LDA model has not been built yet.")

            print("\n--- Topics Discovered ---")
            for idx, topic in self.lda_model.print_topics(num_words=num_words):
                print(f"Topic #{idx + 1}: {topic}")
        except Exception as e:
            print(f"[ERROR] Failed to display topics: {e}")

    def extract_event_phrases(self, phrases=None):
        """
        Extracts headlines that contain any of the specified key phrases.

        Parameters:
        - phrases (list): A list of phrases to match against headlines.
        """
        if phrases is None:
            phrases = ["FDA approval", "price target", "clinical trial", "merger", "earnings", "guidance"]

        try:
            print("\n--- Headlines with Key Phrases ---")
            for idx, headline in enumerate(self.headlines):
                matches = [phrase for phrase in phrases if phrase.lower() in headline.lower()]
                if matches:
                    print(f"Headline {idx + 1}: {headline}")
                    print(f" → Matches: {matches}\n")
        except Exception as e:
            print(f"[ERROR] Failed to extract key phrases: {e}")
