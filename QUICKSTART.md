# 🚀 Quick Start Guide

## Prerequisites
- Python 3.8+ installed
- Node.js 18+ installed
- npm or yarn package manager

## Installation (First Time Only)

### 1. Install Backend Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies
```bash
cd asset-forecaster-pro-main
npm install
cd ..
```

## Running the Application

### Option 1: Automatic Startup (Windows)
Double-click `start_app.bat` - this will start both backend and frontend automatically!

### Option 2: Manual Startup

**Terminal 1 - Backend:**
```bash
python api.py
```

**Terminal 2 - Frontend:**
```bash
cd asset-forecaster-pro-main
npm run dev
```

## Access the Application

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:5000
- **API Health Check:** http://localhost:5000/api/health

## What You'll See

1. **Homepage** with cryptocurrency selector
2. **Overview Tab** - Price charts, statistics, candlestick charts
3. **Technical Analysis Tab** - Volatility, RSI, returns distribution
4. **Forecasting Tab** - ML predictions (ARIMA, Prophet, LSTM)
5. **Correlation Tab** - Correlation heatmap between cryptos

## Testing the Integration

1. Open http://localhost:5173 in your browser
2. Select a cryptocurrency (e.g., BTC)
3. Navigate through different tabs
4. Try generating forecasts
5. Check correlation analysis

## Troubleshooting

**Backend not starting?**
- Make sure port 5000 is not in use
- Check if all Python packages are installed: `pip install -r requirements.txt`

**Frontend not starting?**
- Make sure port 5173 is not in use
- Check if node_modules exists: `cd asset-forecaster-pro-main && npm install`

**API connection errors?**
- Verify backend is running: http://localhost:5000/api/health
- Check `.env` file in `asset-forecaster-pro-main/` folder

## Next Steps

- Read `INTEGRATION_GUIDE.md` for detailed documentation
- Customize the frontend in `asset-forecaster-pro-main/src/`
- Modify API endpoints in `api.py`
- Add more cryptocurrencies by adding CSV files

## 🎉 You're All Set!

The application is now fully integrated and ready to use!
