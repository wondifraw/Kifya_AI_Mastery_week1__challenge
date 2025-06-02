import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns

class StockNewsCorrelationAnalyzer:
    def load_data(file_path):
        return pd.read_csv(file_path)

    def load_and_concatenate_stock_data(file_paths, company_names):
        # List to store individual dataframes
        dataframes = []
        # Loop through each file path and company name
        for file_path, company_name in zip(file_paths, company_names):
            # Load the CSV file
            df = pd.read_csv(file_path)
            # Add a 'Company' column
            df['Company'] = company_name
            # Append the dataframe to the list
            dataframes.append(df)
        # Concatenate all dataframes into one
        stock_df = pd.concat(dataframes)
        return stock_df


    def clean_data(df, date_column):
        # Check if the column name needs to be renamed to 'date'
        if date_column in df.columns:
            df.rename(columns={date_column: 'date'}, inplace=True)
        # Convert the date column to datetime and remove timezone information
        df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.tz_localize(None)
        # Drop rows with any missing values
        df.dropna(inplace=True)
        return df

    def drop_first_column(df):
        df = df.drop(df.columns[0], axis=1)
        return df
    def format_date_column(df, date_column):
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce').dt.strftime('%Y-%m-%d')
        return df




    def merge_data(news_df, stock_df, on='date'):
        merged_df = pd.merge(news_df, stock_df, on=on)
        return merged_df
    def merge_sentiment_with_stock(stock_df, sentiment_df):
        daily_df = pd.merge(stock_df[['date', 'Daily Return']], sentiment_df, on='date', how='inner')
        return daily_df



    def analyze_sentiment(text):
        analysis = TextBlob(text)
        return analysis.sentiment.polarity

    def aggregate_sentiments_by_date(df, date_column='date', sentiment_column='sentiment', output_column='Average Sentiment'):
        daily_sentiment = df.groupby(date_column)[sentiment_column].mean().reset_index()
        daily_sentiment.columns = [date_column, output_column]
        return daily_sentiment

    # Daily Return

    def calculate_daily_returns(df, close_column='Close', return_column='Daily Return'):
        df[return_column] = df[close_column].pct_change() * 100
        return df

    # Stock return

    def calculate_daily_returns(df, close_column='Close', return_column='Daily Return'):
        df[return_column] = df[close_column].pct_change() * 100
        return df

    # Correlation calculation

    def calculate_correlation(df, column1='Average Sentiment', column2='Daily Return'):
        correlation = df[[column1, column2]].corr().iloc[0, 1]
        return correlation


    def plot_daily_returns(daily_df):
        plt.figure(figsize=(14, 7))

        plt.subplot(2, 1, 1)
        plt.plot(daily_df.index, daily_df['Daily Return'], label='Daily Return', color='blue')
        plt.title('Daily Stock Returns')
        plt.xlabel('Date')
        plt.ylabel('Return (%)')
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.plot(daily_df.index, daily_df['Average Sentiment'], label='Average Sentiment', color='orange')
        plt.title('Average Daily Sentiment')
        plt.xlabel('Date')
        plt.ylabel('Sentiment Score')
        plt.legend()

        plt.tight_layout()
        plt.show()

    def scatter_plot(daily_df):
        plt.figure(figsize=(14, 7))
        sns.scatterplot(data=daily_df, x='Average Sentiment', y='Daily Return', alpha=0.5)
        plt.title('Sentiment Score vs. Stock Returns')
        plt.xlabel('Average Sentiment Score')
        plt.ylabel('Daily Return (%)')
        plt.legend()
        plt.show()