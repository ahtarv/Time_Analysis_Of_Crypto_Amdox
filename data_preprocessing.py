import pandas as pd  # library for data manipulation
import numpy as np  # library for numerical operations

class DataPreprocessor:
    """preprocess and clean cryptocurrency data"""
    
    @staticmethod
    def handle_missing_values(df):
        """handle missing values using forward fill then backward fill"""
        # forward fill: copy previous value to fill missing data
        # backward fill: copy next value if forward fill didn't work
        return df.fillna(method='ffill').fillna(method='bfill')
    
    @staticmethod
    def calculate_returns(df, column='close'):
        """calculate daily percentage returns"""
        # pct_change calculates percentage change from previous day
        # formula: (today_price - yesterday_price) / yesterday_price
        df['returns'] = df[column].pct_change()
        return df
    
    @staticmethod
    def calculate_log_returns(df, column='close'):
        """calculate logarithmic returns for better statistical properties"""
        # log returns are better for statistical analysis and compounding
        # formula: ln(today_price / yesterday_price)
        df['log_returns'] = np.log(df[column] / df[column].shift(1))
        return df
    
    @staticmethod
    def calculate_volatility(df, window=30, column='returns'):
        """calculate rolling volatility (annualized standard deviation)"""
        # rolling window calculates std dev over last 30 days
        # multiply by sqrt(365) to annualize daily volatility
        df['volatility'] = df[column].rolling(window=window).std() * np.sqrt(365)
        return df
    
    @staticmethod
    def calculate_moving_averages(df, windows=[7, 30, 90], column='close'):
        """calculate moving averages for trend analysis"""
        # loop through each window size (7, 30, 90 days)
        for window in windows:
            # calculate average price over the window period
            df[f'MA_{window}'] = df[column].rolling(window=window).mean()
        return df
    
    @staticmethod
    def calculate_rsi(df, window=14, column='close'):
        """calculate relative strength index (momentum indicator)"""
        delta = df[column].diff()  # calculate price changes
        # separate gains (positive changes) and losses (negative changes)
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss  # relative strength = average gain / average loss
        # rsi formula: 100 - (100 / (1 + rs))
        # rsi > 70 means overbought, rsi < 30 means oversold
        df['RSI'] = 100 - (100 / (1 + rs))
        return df
    
    @staticmethod
    def prepare_for_modeling(df, column='close'):
        """prepare clean data for time series forecasting models"""
        df_clean = df[[column]].copy()  # create copy with only close price column
        # fill any missing values for model training
        df_clean = df_clean.fillna(method='ffill').fillna(method='bfill')
        return df_clean
