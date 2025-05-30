import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import nltk
from datetime import datetime

nltk.download('stopwords')
from nltk.corpus import stopwords

class EDA_analysis:
    def __init__(self, data):
        self.data = data
        self.stop_words = set(nltk.corpus.stopwords.words('english'))

# Obtain basic statistics for textual lengths (like headline length).

    def descriptive_headline(self):
        """Obtain basic statistics for textual lengths and counts."""
        # Calculate the length of each headline
        self.data['headline_length'] = self.data['headline'].str.len()
        # Get descriptive statistics for headline lengths
        stats = self.data['headline_length'].describe()
        # Count the number of articles per publisher
        article_count_per_publisher = self.data['publisher'].value_counts()
        return stats, article_count_per_publisher
    
# Count the number of articles per publisher to identify which publishers are most active.

    def descriptive_statistics(self):
        # Count the number of articles per publisher
        publisher_counts = self.data['publisher'].value_counts().head(20)
        # Plot article counts per publisher
        plt.figure(figsize=(10, 5))
        publisher_counts.plot(kind='bar', color='green')
        plt.title('Number of Articles per Publisher')
        plt.xlabel('Publisher')
        plt.ylabel('Number of Articles')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.show()


    def analyze_publication_frequency(self):
        """Analyzes publication frequency over time and identifies spikes."""
        if 'date' not in self.data.columns:
            raise ValueError("DataFrame must contain a 'date' column")

        # Convert publication_date to datetime format
        self.data['date'] = pd.to_datetime(self.data['date'], format='%m/%d/%Y %H:%M', errors='coerce')

        # Count frequency of articles per day
        publication_frequency = self.data.set_index('date').resample('D').size()

        # Plot daily publication frequency
        plt.figure(figsize=(12, 6))
        publication_frequency.plot(kind='line', marker='o', color='blue')
        plt.title('Time Series Analysis of Article Publications')
        plt.xlabel('Date')
        plt.ylabel('Number of Articles')
        plt.grid()
        plt.xticks(rotation=45)
        plt.show()

        # Identify spikes in publication frequency
        rolling_mean = publication_frequency.rolling(window=7).mean()
        plt.figure(figsize=(12, 6))
        plt.plot(publication_frequency, label='Daily Publications', color='blue')
        plt.plot(rolling_mean, label='7-Day Rolling Average', color='orange', linewidth=2)
        plt.title('Publication Frequency with Rolling Average')
        plt.xlabel('Date')
        plt.ylabel('Number of Articles')
        plt.legend()
        plt.grid()
        plt.xticks(rotation=45)
        plt.show()

        # Detect and print spikes
        spikes = publication_frequency[publication_frequency > rolling_mean * 1.5]
        print("\nSpikes in Publication Frequency:\n", spikes)



    def analyze_publication_times(self):
        """Analyzes the distribution of publication times and identifies peak publishing hours."""
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
        hourly_counts.plot(kind='bar', color='skyblue')
        plt.title('Publication Frequency by Hour')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Number of Articles')
        plt.xticks(range(24), rotation=0)
        plt.grid(axis='y')
        plt.show()

        # Identify peak hours
        peak_hours = hourly_counts[hourly_counts == hourly_counts.max()]
        print("\nPeak Publishing Hours:\n", peak_hours)




    def time_series_analysis(self):
        # Count frequency of articles per time unit (daily)
        self.data['date'] = pd.to_datetime(self.data['date'], format='%m/%d/%Y %H:%M', errors='coerce')
        publication_frequency = self.data.set_index('date').resample('D').size()

        # Plot time series analysis
        plt.figure(figsize=(12, 6))
        publication_frequency.plot(kind='line', marker='o', color='blue')
        plt.title('Time Series Analysis of Article Publications')
        plt.xlabel('Date')
        plt.ylabel('Number of Articles')
        plt.grid()
        plt.xticks(rotation=45)
        plt.show()

    def publisher_analysis(self):
        # Analyze publisher activity
        publisher_counts = self.data['publisher'].value_counts()
        print("\nTop Publishers:\n", publisher_counts.head())

        # Extract unique domains from publisher names
        self.data['domain'] = self.data['publisher'].apply(lambda x: x.split('@')[-1] if '@' in x else x)
        domain_counts = self.data['domain'].value_counts().head(10)

        # Plot domain contributions
        plt.figure(figsize=(10, 5))
        domain_counts.plot(kind='bar', color='lightgreen')
        plt.title('Publisher Domains Contribution')
        plt.xlabel('Domain')
        plt.ylabel('Number of Articles')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.show()

    def publisher_analysis_Enail(self):
        """Analyze publishers and their contributions."""
        publisher_counts = self.data['publisher'].value_counts()
        unique_domains = self.data['publisher'].str.extract(r'@(.+?)\.')[0].value_counts()
        return publisher_counts, unique_domains