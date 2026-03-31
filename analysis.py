import pandas as pd  # library for data manipulation
import numpy as np  # library for numerical operations
from scipy import stats  # library for statistical functions

class CryptoAnalyzer:
    """analyze cryptocurrency data and calculate metrics"""
    
    @staticmethod
    def calculate_statistics(df, column='close'):
        """calculate basic statistical measures of price data"""
        return {
            'mean': df[column].mean(),  # average price over entire period
            'median': df[column].median(),  # middle value when prices are sorted
            'std': df[column].std(),  # standard deviation (measure of spread)
            'min': df[column].min(),  # lowest price ever recorded
            'max': df[column].max(),  # highest price ever recorded
            'current': df[column].iloc[-1],  # most recent price (last row)
            # calculate total percentage change from first to last price
            'change_pct': ((df[column].iloc[-1] - df[column].iloc[0]) / df[column].iloc[0]) * 100
        }
    
    @staticmethod
    def calculate_volatility_metrics(df):
        """calculate volatility and risk-adjusted return metrics"""
        returns = df['close'].pct_change().dropna()  # calculate daily returns and remove nan
        return {
            'daily_volatility': returns.std(),  # daily price fluctuation
            # annualize volatility by multiplying by sqrt of trading days
            'annual_volatility': returns.std() * np.sqrt(365),
            # sharpe ratio: risk-adjusted return (higher is better)
            # measures return per unit of risk
            'sharpe_ratio': (returns.mean() / returns.std()) * np.sqrt(365) if returns.std() != 0 else 0
        }
    
    @staticmethod
    def detect_trend(df, column='close', window=30):
        """detect if price is in uptrend, downtrend, or sideways"""
        recent_data = df[column].tail(window)  # get last 30 days of data
        # linear regression to find trend line slope
        slope, _, _, _, _ = stats.linregress(range(len(recent_data)), recent_data)
        
        # positive slope means prices going up
        if slope > 0:
            return 'Uptrend'
        # negative slope means prices going down
        elif slope < 0:
            return 'Downtrend'
        # zero slope means prices moving sideways
        else:
            return 'Sideways'
    
    @staticmethod
    def calculate_correlation_matrix(data_dict):
        """calculate how different cryptocurrencies move together"""
        # create dataframe with close prices of all cryptos
        close_prices = pd.DataFrame({ticker: df['close'] for ticker, df in data_dict.items()})
        # correlation: 1 = move together, -1 = move opposite, 0 = no relationship
        return close_prices.corr()
    
    @staticmethod
    def calculate_returns_distribution(df, column='close'):
        """calculate statistical properties of daily returns"""
        returns = df[column].pct_change().dropna()  # calculate daily returns
        return {
            'mean_return': returns.mean(),  # average daily return
            'median_return': returns.median(),  # middle value of returns
            'skewness': returns.skew(),  # asymmetry of distribution (positive = right tail)
            'kurtosis': returns.kurtosis(),  # measure of extreme values (fat tails)
            # percentage of days with positive returns
            'positive_days': (returns > 0).sum() / len(returns) * 100
        }
