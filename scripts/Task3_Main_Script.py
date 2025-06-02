# import sys
# import os

# # Add src directory to the Python path
# src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
# sys.path.append(src_path)

# from src.StockNewsCorrelationAnalyzer import *

# def main():
#     # Load data
#     news_df = StockNewsCorrelationAnalyzer.load_data('../data/news.csv')

#     # File paths and corresponding company names
#     file_paths = [
#         '../data/apple.csv',
#         '../data/amazon.csv',
#         '../data/google.csv',
#         '../data/meta.csv',
#         '../data/microsoft.csv',
#         '../data/nvidia.csv',
#         '../data/tesla.csv'
#     ]

#     company_names = ['Apple', 'Amazon', 'Google', 'Meta', 'Microsoft', 'Nvidia', 'Tesla']

#     # Load and concatenate the stock data
#     stock_df = StockNewsCorrelationAnalyzer.load_and_concatenate_stock_data(file_paths, company_names)

#     # Drop the first column
#     news_df = StockNewsCorrelationAnalyzer.drop_first_column(news_df)
    
#     # Clean data
#     stock_df = StockNewsCorrelationAnalyzer.clean_data(stock_df, 'Date')
#     news_df = StockNewsCorrelationAnalyzer.clean_data(news_df, 'date')
    
#     # Format the 'date' columns
#     news_df = StockNewsCorrelationAnalyzer.format_date_column(news_df, 'date')
#     stock_df = StockNewsCorrelationAnalyzer.format_date_column(stock_df, 'date')

#     # Merge data
#     merged_df = StockNewsCorrelationAnalyzer.merge_data(news_df, stock_df)
    
#     # Analyze sentiment
#     merged_df['sentiment'] = merged_df['headline'].apply(StockNewsCorrelationAnalyzer.analyze_sentiment)
    
#     # Calculate daily stock returns
#     merged_df = StockNewsCorrelationAnalyzer.calculate_daily_returns(merged_df)
    
#     # Aggregate sentiments by date
#     daily_sentiment = StockNewsCorrelationAnalyzer.aggregate_sentiments_by_date(merged_df)
    
#     # Merge sentiment data with stock data
#     daily_df = StockNewsCorrelationAnalyzer.merge_sentiment_with_stock(merged_df, daily_sentiment)

#     # Calculate correlation
#     correlation = StockNewsCorrelationAnalyzer.calculate_correlation(daily_df)
#     print(f'Pearson correlation coefficient: {correlation}')

#     # Visualize
#     StockNewsCorrelationAnalyzer.plot_daily_returns(daily_df)
#     StockNewsCorrelationAnalyzer.scatter_plot(daily_df)

# if __name__ == '__main__':
#     main()