# Cryptocurrency Analysis - Frontend & Backend Integration Guide

## 🎯 Overview

This project integrates a **React TypeScript frontend** with a **Python Flask backend** for cryptocurrency time series analysis and forecasting.

## 📁 Project Structure

```
project-root/
├── api.py                          # Flask REST API backend
├── analysis.py                     # Crypto analysis logic
├── data_loader.py                  # Data loading utilities
├── data_preprocessing.py           # Data preprocessing
├── forecasting_models.py           # ML forecasting models (ARIMA, Prophet, LSTM)
├── visualization.py                # Visualization utilities
├── requirements.txt                # Python dependencies
├── run_api.bat                     # Script to run backend API
├── *.csv                          # Cryptocurrency data files
│
└── asset-forecaster-pro-main/     # React frontend
    ├── src/
    │   ├── lib/
    │   │   ├── api.ts             # API client for backend
    │   │   └── mock-data.ts       # Mock data (fallback)
    │   ├── components/            # React components
    │   ├── pages/                 # Page components
    │   └── types/                 # TypeScript types
    ├── .env                       # Environment variables
    ├── package.json               # Node dependencies
    └── vite.config.ts             # Vite configuration
```

## 🚀 Setup Instructions

### Backend Setup (Python Flask API)

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Flask API server:**
   ```bash
   python api.py
   ```
   Or double-click `run_api.bat` on Windows

3. **Verify the API is running:**
   - Open browser: http://localhost:5000/api/health
   - Should return: `{"status": "ok", "cryptos_loaded": <number>}`

### Frontend Setup (React + Vite)

1. **Navigate to frontend directory:**
   ```bash
   cd asset-forecaster-pro-main
   ```

2. **Install Node dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment variables:**
   - The `.env` file is already created with:
     ```
     VITE_API_URL=http://localhost:5000/api
     ```

4. **Start the development server:**
   ```bash
   npm run dev
   ```

5. **Open the application:**
   - Frontend will run on: http://localhost:5173 (or another port if 5173 is busy)

## 🔌 API Endpoints

### GET `/api/cryptos`
Returns list of available cryptocurrencies
```json
[
  {"symbol": "BTC", "name": "BTC"},
  {"symbol": "ETH", "name": "ETH"}
]
```

### GET `/api/crypto/<ticker>/data`
Returns historical OHLC data with moving averages
```json
[
  {
    "date": "2024-01-01",
    "open": 42000.5,
    "high": 43000.2,
    "low": 41500.8,
    "close": 42500.0,
    "volume": 1234567890,
    "ma7": 42300.5,
    "ma30": 41800.2,
    "ma90": 40500.1
  }
]
```

### GET `/api/crypto/<ticker>/statistics`
Returns price and volatility statistics
```json
{
  "price_statistics": {
    "mean": 42000.5,
    "median": 41800.2,
    "std": 1500.3,
    "min": 38000.0,
    "max": 45000.0,
    "current": 42500.0,
    "change_pct": 2.5
  },
  "volatility_metrics": {
    "daily_volatility": 0.025,
    "annual_volatility": 0.48,
    "sharpe_ratio": 1.25
  }
}
```

### GET `/api/crypto/<ticker>/technical`
Returns technical analysis data (trend, volatility, RSI, returns)
```json
{
  "trend": "Uptrend",
  "volatility": [{"date": "2024-01-01", "value": 0.025}],
  "returns_distribution": [{"bin": "-5%", "count": 10}],
  "returns_stats": {
    "mean_return": 0.001,
    "median_return": 0.0008,
    "skewness": 0.15,
    "kurtosis": 2.5,
    "positive_days": 55.2
  },
  "rsi": [{"date": "2024-01-01", "value": 65.5}]
}
```

### POST `/api/forecast`
Generates price forecasts using ML models
```json
// Request
{
  "ticker": "BTC",
  "days": 30,
  "models": ["arima", "prophet", "lstm"]
}

// Response
[
  {
    "model": "ARIMA",
    "predictions": [
      {"date": "2024-02-01", "price": 43000.5}
    ]
  }
]
```

### POST `/api/correlation`
Calculates correlation matrix between cryptocurrencies
```json
// Request
{
  "tickers": ["BTC", "ETH", "ADA"]
}

// Response
{
  "tickers": ["BTC", "ETH", "ADA"],
  "matrix": [
    [1.0, 0.85, 0.72],
    [0.85, 1.0, 0.68],
    [0.72, 0.68, 1.0]
  ]
}
```

## 🔧 Configuration

### Backend Configuration (api.py)
- **Port:** 5000 (default Flask port)
- **CORS:** Enabled for all origins (development mode)
- **Debug:** Enabled (set to False for production)

### Frontend Configuration (.env)
- **VITE_API_URL:** Backend API base URL
- Change to production URL when deploying

## 🎨 Frontend Features

1. **Overview Tab**
   - Real-time price metrics
   - Interactive price charts with moving averages
   - Candlestick charts
   - Statistical summaries

2. **Technical Analysis Tab**
   - Trend detection
   - Volatility analysis
   - Returns distribution
   - RSI indicator

3. **Forecasting Tab**
   - Multi-model forecasting (ARIMA, Prophet, LSTM)
   - Adjustable forecast period (7-90 days)
   - Visual comparison of model predictions

4. **Correlation Analysis Tab**
   - Multi-crypto correlation heatmap
   - Correlation matrix table

## 🐛 Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError`
```bash
# Solution: Install missing dependencies
pip install -r requirements.txt
```

**Problem:** Port 5000 already in use
```python
# Solution: Change port in api.py
app.run(debug=True, port=5001)  # Use different port
```

**Problem:** CORS errors
```python
# Solution: Verify CORS is enabled in api.py
from flask_cors import CORS
CORS(app)
```

### Frontend Issues

**Problem:** API connection refused
```bash
# Solution: Ensure backend is running
python api.py

# Check .env file has correct API URL
VITE_API_URL=http://localhost:5000/api
```

**Problem:** Module not found
```bash
# Solution: Install dependencies
cd asset-forecaster-pro-main
npm install
```

**Problem:** Port 5173 in use
```bash
# Vite will automatically use next available port
# Check terminal output for actual port number
```

## 📦 Production Deployment

### Backend Deployment
1. Set `debug=False` in api.py
2. Use production WSGI server (gunicorn, waitress)
3. Configure proper CORS origins
4. Set up environment variables
5. Use production database if needed

### Frontend Deployment
1. Build production bundle:
   ```bash
   npm run build
   ```
2. Deploy `dist/` folder to hosting service
3. Update `.env` with production API URL
4. Configure CORS on backend for production domain

## 🔐 Security Notes

- **CORS:** Currently allows all origins (development only)
- **API Keys:** Add authentication for production
- **Rate Limiting:** Implement rate limiting for API endpoints
- **Input Validation:** Add validation for user inputs
- **HTTPS:** Use HTTPS in production

## 📊 Data Flow

```
User Interaction (React Frontend)
        ↓
API Request (fetch)
        ↓
Flask Backend (api.py)
        ↓
Data Processing (analysis.py, preprocessing.py)
        ↓
ML Models (forecasting_models.py)
        ↓
JSON Response
        ↓
React State Update
        ↓
UI Rendering (Charts, Tables)
```

## 🎯 Next Steps

1. ✅ Backend API created
2. ✅ Frontend API client created
3. ✅ Environment configuration
4. 🔄 Update frontend components to use real API
5. 🔄 Test all endpoints
6. 🔄 Add error handling
7. 🔄 Add loading states
8. 🔄 Deploy to production

## 📝 Notes

- The frontend currently uses mock data in `mock-data.ts`
- To use real backend data, update components to import from `lib/api.ts`
- All ML models run on-demand (may take 2-5 seconds)
- LSTM training can be slow (30 epochs)
- Consider caching forecast results for better performance

## 🤝 Support

For issues or questions:
1. Check API health endpoint: http://localhost:5000/api/health
2. Check browser console for errors
3. Check Flask terminal for backend errors
4. Verify all dependencies are installed
