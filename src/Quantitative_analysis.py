import pandas as pd
import talib
import matplotlib.pyplot as plt

class Quantitative_analysis:
    def __init__(self, file_path):
        """
        Initialize the Quantitative_analysis with a file path to a CSV file.

        Parameters:
            file_path (str): The path to the CSV file containing stock data.
        """
        self.file_path = file_path
        self.data = None

    def __init__(self, file_paths):
        self.file_paths = file_paths
        self.data = None

    def load_data(self):
        """Load stock price data into pandas DataFrames from CSV files."""
        try:
            dataframes = []
            for file_path in self.file_paths:
                df = pd.read_csv(file_path)
                required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                if not all(col in df.columns for col in required_columns):
                    raise ValueError(f"CSV file {file_path} must contain required columns.")
                dataframes.append(df)

            # Combine DataFrames
            self.data = pd.concat(dataframes, ignore_index=True)
            print(f"Combined data loaded: {self.data.shape[0]} rows.")
        except Exception as e:
            print(f"Error loading data: {e}")

    def apply_technical_indicators(self):
        """Calculate technical indicators using TA-Lib."""
        if self.data is None:
            print("Data is not loaded. Please load the data first.")
            return

        try:
            self.data['MA20'] = talib.SMA(self.data['Close'], timeperiod=20)
            self.data['MA50'] = talib.SMA(self.data['Close'], timeperiod=50)
            self.data['RSI'] = talib.RSI(self.data['Close'], timeperiod=14)
            self.data['MACD'], self.data['MACD_signal'], _ = talib.MACD(self.data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
            print("Technical indicators calculated.")
        except Exception as e:
            print(f"Error calculating indicators: {e}")

    def visualize_data(self):
        """Visualize stock price and indicators using matplotlib."""
        if self.data is None:
            print("Data is not loaded. Please load the data first.")
            return
            
        try:
            # Create a figure with subplots
            fig, axs = plt.subplots(3, 1, figsize=(14, 12))

            # Plot the stock price and moving averages
            axs[0].plot(self.data['Close'], label='Close Price', color='blue')
            axs[0].plot(self.data['MA20'], label='20-Day MA', color='orange')
            axs[0].plot(self.data['MA50'], label='50-Day MA', color='green')
            axs[0].set_title('Stock Price and Moving Averages')
            axs[0].set_ylabel('Price')
            axs[0].legend()
            axs[0].grid()

            # Plot RSI
            axs[1].plot(self.data['RSI'], label='RSI', color='purple')
            axs[1].axhline(70, linestyle='--', alpha=0.5, color='red')
            axs[1].axhline(30, linestyle='--', alpha=0.5, color='green')
            axs[1].set_title('Relative Strength Index (RSI)')
            axs[1].set_ylabel('RSI')
            axs[1].legend()
            axs[1].grid()

            # Plot MACD
            axs[2].plot(self.data['MACD'], label='MACD', color='blue')
            axs[2].plot(self.data['MACD_signal'], label='MACD Signal', color='orange')
            axs[2].set_title('MACD (Moving Average Convergence Divergence)')
            axs[2].set_ylabel('MACD')
            axs[2].legend()
            axs[2].grid()

            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Error during visualization: {e}")

# Example usage
# if __name__ == "__main__":
#     file_path = 'path/to/your/stock_data.csv'  # Replace with your CSV file path
#     stock_analyzer = StockAnalyzer(file_path)

#     # Load data from the CSV file
#     stock_analyzer.load_data()

#     # Apply technical indicators
#     stock_analyzer.apply_technical_indicators()

#     # Visualize the stock data and indicators
#     stock_analyzer.visualize_data()