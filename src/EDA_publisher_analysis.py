import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import nltk
from datetime import datetime

nltk.download('stopwords')
from nltk.corpus import stopwords

class EDA_publisher_analysis:
    def __init__(self, data):
        self.data = data
        """Initialize the EDA_analysis class.

        Parameters:
            data (DataFrame): The input DataFrame containing articles with headlines, publishers, and dates.
        """
        self.data = data
        self.stop_words = set(nltk.corpus.stopwords.words('english'))

    def descriptive_headline(self):
        """Obtain basic statistics for textual lengths and counts.

        Returns:
            tuple: Descriptive statistics of headline lengths (Series) and article counts per publisher (Series).
        """
        try:
            self.data['headline_length'] = self.data['headline'].str.len()
            stats = self.data['headline_length'].describe()
            return stats
        except Exception as e:
            print(f"Error in descriptive_headline: {e}")


    def descriptive_statistics(self):
        """Count the number of articles per publisher to identify which publishers are most active."""
        try:
            publisher_counts = self.data['publisher'].value_counts().head(20)
            plt.figure(figsize=(10, 5))
            publisher_counts.plot(kind='bar', color='green')
            plt.title('Number of Articles per Publisher')
            plt.xlabel('Publisher')
            plt.ylabel('Number of Articles')
            plt.xticks(rotation=45)
            plt.grid(axis='y')
            plt.show()
        except Exception as e:
            print(f"Error in descriptive_statistics: {e}")
        

    def analyze_publication_trends(self):
        """Analyze publication dates to identify trends in news frequency over time.

        This function examines the frequency of articles published on each day and visualizes
        the trends. It can help identify days with increased publication activity, which may correlate
        with specific events or trends.

        Raises:
            ValueError: If 'date' column is not present in the DataFrame.
        """
        try:
            if 'date' not in self.data.columns:
                raise ValueError("DataFrame must contain a 'date' column")

            # Convert publication_date to datetime format
            self.data['date'] = pd.to_datetime(self.data['date'], format='%m/%d/%Y %H:%M', errors='coerce')

            # Count frequency of articles per day
            publication_trends = self.data.set_index('date').resample('D').size()

            # Plot publication trends over time
            plt.figure(figsize=(12, 6))
            publication_trends.plot(kind='line', marker='o', color='purple')
            plt.title('Trends in Article Publications Over Time')
            plt.xlabel('Date')
            plt.ylabel('Number of Articles')
            plt.grid()
            plt.xticks(rotation=45)
            plt.show()
            # Print summary of trends
            print("\nPublication Trends Summary:\n", publication_trends.describe())
        except Exception as e:
            print(f"Error in analyze_publication_trends: {e}")
    

    def clean_data(self):
        """
        Clean the text data by removing numeric values and outliers from the 'headline' column.

        This function modifies the DataFrame in place by applying regex to remove unwanted characters.
        """
        try:
            # Remove numeric values and punctuation
            self.data['headline'] = self.data['headline'].apply(lambda x: re.sub(r'\d+', '', x))  # Remove numbers
            self.data['headline'] = self.data['headline'].apply(lambda x: re.sub(r'[^\w\s]', '', x))  # Remove punctuation
            
            # Remove rows with empty headlines
            self.data = self.data[self.data['headline'].str.strip() != '']
            print("Data cleaning completed.")
        except Exception as e:
            print(f"Error in clean_data: {e}")
    

    def analyze_topics_in_articles(self, num_topics=5, num_keywords=10):
        """Perform topic modeling to identify common keywords and phrases in articles.

        This function uses natural language processing techniques to extract topics and significant
        events from the text of articles. It applies Count Vectorization followed by Latent Dirichlet
        Allocation (LDA) to identify common keywords associated with each topic. The results are then
        visualized in a bar chart.

        Parameters:
            num_topics (int): The number of topics to identify (default is 5).
            num_keywords (int): The number of keywords to extract for each topic (default is 10).

        Raises:
            ValueError: If 'text' column is not present in the DataFrame.
        """
        try:
            if 'headline' not in self.data.columns:
                raise ValueError("DataFrame must contain a 'headline' column")

            # Vectorize the text data
            vectorizer = CountVectorizer(stop_words='english')
            text_matrix = vectorizer.fit_transform(self.data['headline'])

            # Apply LDA for topic modeling
            lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
            lda.fit(text_matrix)

            # Retrieve the words associated with each topic
            keywords = vectorizer.get_feature_names_out()
            topics = []
            for index, topic in enumerate(lda.components_):
                top_keywords = [keywords[i] for i in topic.argsort()[-num_keywords:]]
                topics.append(f"Topic {index + 1}: {', '.join(top_keywords)}")
            
            # Plot the identified topics
            self.plot_identified_topics(topics)

        except Exception as e:
            print(f"Error in analyze_topics_in_articles: {e}")
    def plot_identified_topics(self, topics):
        """Plot the identified topics in a bar chart.
        This function visualizes the identified topics using a horizontal bar chart.

        Parameters:
            topics (list): A list of strings representing the identified topics.
        """
        try:
            plt.figure(figsize=(10, 6))
            counts = [1] * len(topics)  # Uniform frequency for visualization
            plt.barh(range(len(topics)), counts, tick_label=topics, color='green')
            plt.title('Identified Topics')
            plt.xlabel('Frequency')
            plt.xlim(0, 1)  # Set x-axis limits for uniformity
            plt.grid(axis='x')
            plt.show()
        except Exception as e:
            print(f"Error in plot_identified_topics: {e}")


    def analyze_publication_frequency_variation(self):
        """Analyze how publication frequency varies over time and identify spikes related to market events.

        This function examines the frequency of articles published over time and highlights
        any significant spikes in publication activity. These spikes may correlate with specific
        market events or trends.

        Raises:
            ValueError: If 'date' column is not present in the DataFrame.
        """
        try:
            if 'date' not in self.data.columns:
                raise ValueError("DataFrame must contain a 'date' column")

            # Convert publication_date to datetime format
            self.data['date'] = pd.to_datetime(self.data['date'], format='%m/%d/%Y %H:%M', errors='coerce')

            # Count frequency of articles per day
            publication_frequency = self.data.set_index('date').resample('D').size()

            # Plot publication frequency over time
            plt.figure(figsize=(12, 6))
            publication_frequency.plot(kind='line', marker='o', color='blue')
            plt.title('Publication Frequency Over Time')
            plt.xlabel('Date')
            plt.ylabel('Number of Articles')
            plt.grid()
            plt.xticks(rotation=45)
            plt.show()

            # Identify and print spikes in publication frequency
            rolling_mean = publication_frequency.rolling(window=7).mean()
            spikes = publication_frequency[publication_frequency > rolling_mean * 1.5]
            print("\nSpikes in Publication Frequency:\n", spikes)
        except Exception as e:
            print(f"Error in analyze_publication_frequency_variation: {e}")



    def analyze_publication_times_for_trading(self):
        """Analyze publication times to identify peak hours for news releases.

        This function examines the distribution of article publication times to determine
        if there are specific hours during which most news is released. Understanding these
        peak times can be crucial for traders and automated trading systems.

        Raises:
            ValueError: If 'date' column is not present in the DataFrame.
        """
        try:
            if 'date' not in self.data.columns:
                raise ValueError("DataFrame must contain a 'date' column")

            # Convert publication_date to datetime format
            self.data['date'] = pd.to_datetime(self.data['date'], format='%m/%d/%Y %H:%M', errors='coerce')

            # Extract hour from publication_date
            self.data['publication_hour'] = self.data['date'].dt.hour

            # Count publications per hour
            hourly_counts = self.data['publication_hour'].value_counts().sort_index()

            # Plot publication counts by hour
            plt.figure(figsize=(12, 6))
            hourly_counts.plot(kind='bar', color='blue')
            plt.title('Publication Frequency by Hour')
            plt.xlabel('Hour of the Day')
            plt.ylabel('Number of Articles')
            plt.xticks(range(24), rotation=0)
            plt.grid(axis='y')
            plt.show()

            # Identify and print peak hours
            peak_hours = hourly_counts[hourly_counts == hourly_counts.max()]
            print("\nPeak Publishing Hours:\n", peak_hours)
        except Exception as e:
            print(f"Error in analyze_publication_times_for_trading: {e}")


    
    def analyze_publishers_contribution(self):
        """Analyze publisher contributions to the news feed and the types of news reported.

        This function identifies the top publishers based on the number of articles they contribute
        and examines the differences in the types of news reported by these publishers. This analysis
        can provide insights into the media landscape and the focus areas of different publishers.

        Raises:
            ValueError: If 'publisher' column is not present in the DataFrame.
        """
        try:
            if 'publisher' not in self.data.columns:
                raise ValueError("DataFrame must contain a 'publisher' column")

            # Count the number of articles per publisher
            publisher_counts = self.data['publisher'].value_counts()
            top_publishers = publisher_counts.head(10)

            # Display top publishers
            print("\nTop Publishers:\n", top_publishers)
        except Exception as e:
            print(f"Error in analyze_publishers_contribution: {e}")



    def analyze_unique_domains_from_publishers(self):

        """Identify unique domains from publisher names to analyze contribution frequency.

        This function extracts domains from publisher names that are formatted as email addresses
        and counts the frequency of contributions from each unique domain. This analysis helps
        to understand which organizations are contributing most frequently to the news feed.

        Raises:
            ValueError: If 'publisher' column is not present in the DataFrame.
        """
        try:
            if 'publisher' not in self.data.columns:
                raise ValueError("DataFrame must contain a 'publisher' column")

            # Extract unique domains from publisher names
            self.data['domain'] = self.data['publisher'].str.extract(r'@(.+?)(?:\.|$)')[0]
            
            # Count the number of articles per domain
            domain_counts = self.data['domain'].value_counts()

            # Display top domains
            print("\nTop Domains Contributing to News Feed:\n", domain_counts.head(10))

            # Optionally, plot the contributions of top domains
            plt.figure(figsize=(10, 5))
            domain_counts.head(10).plot(kind='bar', color='lightblue')
            plt.title('Top Domains Contributing to News Feed')
            plt.xlabel('Domain')
            plt.ylabel('Number of Articles')
            plt.xticks(rotation=45)
            plt.grid(axis='y')
            plt.show()
        except Exception as e:
            print(f"Error in analyze_unique_domains_from_publishers: {e}")











    