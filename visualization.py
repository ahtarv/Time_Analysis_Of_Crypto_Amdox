import plotly.graph_objects as go  # library for interactive charts
import plotly.express as px  # high-level plotting library
from plotly.subplots import make_subplots  # create multiple charts in one figure
import pandas as pd  # data manipulation library

class CryptoVisualizer:
    """visualization utilities for cryptocurrency data"""
    
    @staticmethod
    def plot_price_trend(df, ticker, show_ma=True):
        """plot price trend line with optional moving averages"""
        fig = go.Figure()  # create empty figure
        
        # add main price line (blue line showing close prices)
        fig.add_trace(go.Scatter(x=df.index, y=df['close'], 
                                 mode='lines', name='close price',
                                 line=dict(color='blue', width=2)))
        
        # add moving average lines if they exist in dataframe
        if show_ma and 'MA_7' in df.columns:
            # 7-day moving average (orange line)
            fig.add_trace(go.Scatter(x=df.index, y=df['MA_7'], 
                                     mode='lines', name='ma 7',
                                     line=dict(color='orange', width=1)))
            # 30-day moving average (green line)
            fig.add_trace(go.Scatter(x=df.index, y=df['MA_30'], 
                                     mode='lines', name='ma 30',
                                     line=dict(color='green', width=1)))
        
        # customize chart appearance
        fig.update_layout(title=f'{ticker} price trend',
                         xaxis_title='date', yaxis_title='price (usd)',
                         hovermode='x unified', template='plotly_white')
        return fig
    
    @staticmethod
    def plot_candlestick(df, ticker):
        """plot candlestick chart (shows open, high, low, close)"""
        # candlestick chart: green candle = price up, red candle = price down
        fig = go.Figure(data=[go.Candlestick(x=df.index,
                                             open=df['open'],  # opening price
                                             high=df['high'],  # highest price
                                             low=df['low'],  # lowest price
                                             close=df['close'])])  # closing price
        
        fig.update_layout(title=f'{ticker} candlestick chart',
                         xaxis_title='date', yaxis_title='price (usd)',
                         template='plotly_white')
        return fig
    
    @staticmethod
    def plot_volume(df, ticker):
        """plot trading volume as bar chart"""
        fig = go.Figure()
        # bar chart showing how much was traded each day
        fig.add_trace(go.Bar(x=df.index, y=df.get('volume', []),
                            name='volume', marker_color='lightblue'))
        
        fig.update_layout(title=f'{ticker} trading volume',
                         xaxis_title='date', yaxis_title='volume',
                         template='plotly_white')
        return fig
    
    @staticmethod
    def plot_returns_distribution(df):
        """plot histogram of daily returns distribution"""
        # calculate daily returns (percentage change)
        returns = df['close'].pct_change().dropna()
        
        fig = go.Figure()
        # histogram shows frequency of different return values
        fig.add_trace(go.Histogram(x=returns, nbinsx=50, 
                                   name='returns distribution',
                                   marker_color='steelblue'))
        
        fig.update_layout(title='daily returns distribution',
                         xaxis_title='returns', yaxis_title='frequency',
                         template='plotly_white')
        return fig
    
    @staticmethod
    def plot_volatility(df, ticker):
        """plot volatility over time (shows risk level)"""
        fig = go.Figure()
        # volatility line shows how much price fluctuates
        # higher volatility = more risky
        fig.add_trace(go.Scatter(x=df.index, y=df['volatility'],
                                mode='lines', name='volatility',
                                line=dict(color='red', width=2)))
        
        fig.update_layout(title=f'{ticker} volatility (30-day)',
                         xaxis_title='date', yaxis_title='volatility',
                         template='plotly_white')
        return fig
    
    @staticmethod
    def plot_correlation_heatmap(corr_matrix):
        """plot correlation heatmap between cryptocurrencies"""
        # heatmap shows which cryptos move together
        # red = positive correlation, blue = negative correlation
        fig = go.Figure(data=go.Heatmap(z=corr_matrix.values,
                                        x=corr_matrix.columns,
                                        y=corr_matrix.index,
                                        colorscale='RdBu',  # red-blue color scale
                                        zmid=0))  # center at zero
        
        fig.update_layout(title='cryptocurrency correlation matrix',
                         template='plotly_white',
                         height=800, width=800)
        return fig
    
    @staticmethod
    def plot_forecast_comparison(df, forecasts, ticker):
        """plot actual prices vs forecasted prices from different models"""
        fig = go.Figure()
        
        # plot actual historical prices (solid blue line)
        fig.add_trace(go.Scatter(x=df.index, y=df['close'],
                                mode='lines', name='actual',
                                line=dict(color='blue', width=2)))
        
        # plot forecasts from each model (dashed lines)
        colors = ['red', 'green', 'orange']  # different color for each model
        for i, (model_name, forecast_data) in enumerate(forecasts.items()):
            # add forecast line with dashed style
            fig.add_trace(go.Scatter(x=forecast_data['dates'], 
                                    y=forecast_data['values'],
                                    mode='lines', name=f'{model_name} forecast',
                                    line=dict(color=colors[i], width=2, dash='dash')))
        
        fig.update_layout(title=f'{ticker} price forecast comparison',
                         xaxis_title='date', yaxis_title='price (usd)',
                         hovermode='x unified', template='plotly_white')
        return fig
