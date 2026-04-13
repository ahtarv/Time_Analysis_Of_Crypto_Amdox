from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data_loader import CryptoDataLoader
from data_preprocessing import DataPreprocessor
from analysis import CryptoAnalyzer
from forecasting_models import ARIMAForecaster, ProphetForecaster, LSTMForecaster
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize components
loader = CryptoDataLoader('.')
crypto_data, available_tickers = loader.load_all_cryptos(), loader.get_available_tickers()
preprocessor = DataPreprocessor()
analyzer = CryptoAnalyzer()

@app.route('/api/cryptos', methods=['GET'])
def get_cryptos():
    """Get list of available cryptocurrency tickers"""
    tickers = [{"symbol": ticker, "name": ticker} for ticker in available_tickers]
    return jsonify(tickers)

@app.route('/api/crypto/<ticker>/data', methods=['GET'])
def get_crypto_data(ticker):
    """Get historical OHLC data for a cryptocurrency"""
    if ticker not in crypto_data:
        return jsonify({"error": "Ticker not found"}), 404
    
    df = crypto_data[ticker].copy()
    
    # Preprocess data
    df = preprocessor.handle_missing_values(df)
    df = preprocessor.calculate_returns(df)
    df = preprocessor.calculate_log_returns(df)
    df = preprocessor.calculate_volatility(df)
    df = preprocessor.calculate_moving_averages(df)
    df = preprocessor.calculate_rsi(df)
    
    # Convert to JSON format
    df_reset = df.reset_index()
    data = []
    for _, row in df_reset.iterrows():
        data.append({
            "date": row['date'].strftime('%Y-%m-%d'),
            "open": float(row.get('open', row['close'])),
            "high": float(row.get('high', row['close'])),
            "low": float(row.get('low', row['close'])),
            "close": float(row['close']),
            "volume": int(row.get('volume', 0)),
            "ma7": float(row['MA_7']) if pd.notna(row.get('MA_7')) else None,
            "ma30": float(row['MA_30']) if pd.notna(row.get('MA_30')) else None,
            "ma90": float(row['MA_90']) if pd.notna(row.get('MA_90')) else None,
        })
    
    return jsonify(data)

@app.route('/api/crypto/<ticker>/statistics', methods=['GET'])
def get_statistics(ticker):
    """Get price statistics for a cryptocurrency"""
    if ticker not in crypto_data:
        return jsonify({"error": "Ticker not found"}), 404
    
    df = crypto_data[ticker].copy()
    df = preprocessor.handle_missing_values(df)
    
    stats = analyzer.calculate_statistics(df)
    vol_metrics = analyzer.calculate_volatility_metrics(df)
    
    return jsonify({
        "price_statistics": stats,
        "volatility_metrics": vol_metrics
    })

@app.route('/api/crypto/<ticker>/technical', methods=['GET'])
def get_technical(ticker):
    """Get technical analysis data for a cryptocurrency"""
    if ticker not in crypto_data:
        return jsonify({"error": "Ticker not found"}), 404
    
    df = crypto_data[ticker].copy()
    df = preprocessor.handle_missing_values(df)
    df = preprocessor.calculate_returns(df)
    df = preprocessor.calculate_volatility(df)
    df = preprocessor.calculate_rsi(df)
    
    # Trend detection
    trend = analyzer.detect_trend(df)
    
    # Volatility data (last 90 days)
    volatility_data = []
    df_reset = df.reset_index()
    for _, row in df_reset.tail(90).iterrows():
        if pd.notna(row.get('volatility')):
            volatility_data.append({
                "date": row['date'].strftime('%Y-%m-%d'),
                "value": float(row['volatility'])
            })
    
    # Returns distribution
    returns = df['close'].pct_change().dropna() * 100
    bins = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
    distribution = []
    for i in range(len(bins)):
        lo = float('-inf') if i == 0 else bins[i]
        hi = float('inf') if i == len(bins) - 1 else bins[i + 1] if i < len(bins) - 1 else bins[i]
        count = len(returns[(returns >= lo) & (returns < hi)])
        distribution.append({"bin": f"{bins[i]}%", "count": count})
    
    # Returns statistics
    returns_stats = analyzer.calculate_returns_distribution(df)
    
    # RSI data (last 90 days)
    rsi_data = []
    for _, row in df_reset.tail(90).iterrows():
        if pd.notna(row.get('RSI')):
            rsi_data.append({
                "date": row['date'].strftime('%Y-%m-%d'),
                "value": float(row['RSI'])
            })
    
    return jsonify({
        "trend": trend,
        "volatility": volatility_data,
        "returns_distribution": distribution,
        "returns_stats": returns_stats,
        "rsi": rsi_data
    })

@app.route('/api/forecast', methods=['POST'])
def generate_forecast():
    """Generate price forecasts using selected models"""
    data = request.json
    ticker = data.get('ticker')
    days = data.get('days', 30)
    models = data.get('models', ['arima', 'prophet'])
    
    if ticker not in crypto_data:
        return jsonify({"error": "Ticker not found"}), 404
    
    df = crypto_data[ticker].copy()
    df = preprocessor.handle_missing_values(df)
    df_clean = preprocessor.prepare_for_modeling(df)
    
    results = []
    
    # ARIMA
    if 'arima' in [m.lower() for m in models]:
        try:
            arima = ARIMAForecaster()
            arima.fit(df_clean['close'])
            forecast = arima.forecast(steps=days)
            
            predictions = []
            for i in range(days):
                date = df.index[-1] + timedelta(days=i+1)
                predictions.append({
                    "date": date.strftime('%Y-%m-%d'),
                    "price": float(forecast.iloc[i])
                })
            
            results.append({"model": "ARIMA", "predictions": predictions})
        except Exception as e:
            print(f"ARIMA error: {e}")
    
    # Prophet
    if 'prophet' in [m.lower() for m in models]:
        try:
            prophet = ProphetForecaster()
            prophet.fit(df_clean)
            forecast = prophet.forecast(periods=days)
            
            predictions = []
            for _, row in forecast.tail(days).iterrows():
                predictions.append({
                    "date": row['ds'].strftime('%Y-%m-%d'),
                    "price": float(row['yhat'])
                })
            
            results.append({"model": "Prophet", "predictions": predictions})
        except Exception as e:
            print(f"Prophet error: {e}")
    
    # LSTM
    if 'lstm' in [m.lower() for m in models]:
        try:
            lstm = LSTMForecaster(lookback=60)
            lstm.fit(df_clean['close'], epochs=30)
            forecast = lstm.forecast(df_clean['close'], steps=days)
            
            predictions = []
            for i in range(days):
                date = df.index[-1] + timedelta(days=i+1)
                predictions.append({
                    "date": date.strftime('%Y-%m-%d'),
                    "price": float(forecast[i])
                })
            
            results.append({"model": "LSTM", "predictions": predictions})
        except Exception as e:
            print(f"LSTM error: {e}")
    
    return jsonify(results)

@app.route('/api/correlation', methods=['POST'])
def get_correlation():
    """Calculate correlation matrix for selected cryptocurrencies"""
    data = request.json
    tickers = data.get('tickers', [])
    
    if len(tickers) < 2:
        return jsonify({"error": "At least 2 tickers required"}), 400
    
    # Filter available data
    filtered_data = {ticker: crypto_data[ticker] for ticker in tickers if ticker in crypto_data}
    
    if len(filtered_data) < 2:
        return jsonify({"error": "Not enough valid tickers"}), 400
    
    # Calculate correlation
    corr_matrix = analyzer.calculate_correlation_matrix(filtered_data)
    
    return jsonify({
        "tickers": list(corr_matrix.columns),
        "matrix": corr_matrix.values.tolist()
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok", "cryptos_loaded": len(available_tickers)})

if __name__ == '__main__':
    print(f"Loaded {len(available_tickers)} cryptocurrencies")
    print("Starting Flask API server...")
    app.run(debug=True, port=5000)
