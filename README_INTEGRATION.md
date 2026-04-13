# 📈 Cryptocurrency Time Series Analysis Platform

A full-stack application combining **Python machine learning** with a **modern React frontend** for cryptocurrency analysis and forecasting.

## 🌟 Features

### Backend (Python + Flask)
- **Data Analysis:** Statistical analysis of cryptocurrency price data
- **Technical Indicators:** RSI, Moving Averages, Volatility metrics
- **ML Forecasting:** ARIMA, Prophet, and LSTM models
- **Correlation Analysis:** Multi-crypto correlation matrices
- **REST API:** 7 endpoints serving real-time data

### Frontend (React + TypeScript)
- **Overview Dashboard:** Price charts, candlesticks, statistics
- **Technical Analysis:** Volatility, returns distribution, RSI
- **Forecasting:** Interactive ML predictions with multiple models
- **Correlation Heatmap:** Visual correlation analysis
- **Modern UI:** Built with Tailwind CSS and shadcn/ui

## 🚀 Quick Start

### 1. Install Dependencies

**Backend:**
```bash
pip install -r requirements.txt
```

**Frontend:**
```bash
cd asset-forecaster-pro-main
npm install
cd ..
```

### 2. Verify Setup
```bash
python verify_setup.py
```

### 3. Start Application

**Option A - Automatic (Windows):**
```bash
# Double-click start_app.bat
```

**Option B - Manual:**
```bash
# Terminal 1 - Backend
python api.py

# Terminal 2 - Frontend
cd asset-forecaster-pro-main
npm run dev
```

### 4. Access Application
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:5000
- **Health Check:** http://localhost:5000/api/health

## 📁 Project Structure

```
project-root/
├── Backend (Python)
│   ├── api.py                      # Flask REST API
│   ├── analysis.py                 # Analysis logic
│   ├── data_loader.py              # Data loading
│   ├── data_preprocessing.py       # Preprocessing
│   ├── forecasting_models.py       # ML models
│   ├── visualization.py            # Visualization utils
│   └── *.csv                       # Crypto data
│
├── Frontend (React)
│   └── asset-forecaster-pro-main/
│       ├── src/
│       │   ├── components/         # React components
│       │   ├── lib/
│       │   │   ├── api.ts         # API client
│       │   │   └── mock-data.ts   # Mock data
│       │   ├── pages/             # Page components
│       │   └── types/             # TypeScript types
│       ├── .env                   # Environment config
│       └── package.json           # Dependencies
│
├── Scripts
│   ├── start_app.bat              # Start both servers
│   ├── run_api.bat                # Start backend only
│   ├── verify_setup.py            # Verify installation
│   └── test_api.py                # Test API endpoints
│
└── Documentation
    ├── README_INTEGRATION.md      # This file
    ├── INTEGRATION_GUIDE.md       # Detailed guide
    ├── QUICKSTART.md              # Quick start
    └── INTEGRATION_SUMMARY.md     # Summary
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/cryptos` | GET | List cryptocurrencies |
| `/api/crypto/<ticker>/data` | GET | OHLC data + MAs |
| `/api/crypto/<ticker>/statistics` | GET | Price & volatility stats |
| `/api/crypto/<ticker>/technical` | GET | Technical analysis |
| `/api/forecast` | POST | Generate forecasts |
| `/api/correlation` | POST | Correlation matrix |

## 🧪 Testing

### Test API Endpoints
```bash
python test_api.py
```

### Manual Testing
1. Start both servers
2. Open http://localhost:5173
3. Select a cryptocurrency
4. Navigate through tabs
5. Generate forecasts
6. Check correlation analysis

## 📊 Technology Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Statsmodels** - ARIMA forecasting
- **Prophet** - Time series forecasting
- **TensorFlow** - LSTM neural networks
- **Scikit-learn** - ML utilities

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **shadcn/ui** - Component library
- **Recharts** - Data visualization
- **React Query** - Data fetching
- **React Router** - Navigation

## 🎯 Usage Examples

### Analyze Bitcoin
1. Select "BTC" from dropdown
2. View Overview tab for price trends
3. Check Technical Analysis for RSI and volatility
4. Generate 30-day forecast using ARIMA and Prophet
5. Compare with other cryptos in Correlation tab

### Generate Forecasts
```typescript
// Frontend API call
const forecasts = await generateForecast("BTC", 30, ["arima", "prophet", "lstm"]);
```

```python
# Backend API call
POST /api/forecast
{
  "ticker": "BTC",
  "days": 30,
  "models": ["arima", "prophet", "lstm"]
}
```

### Correlation Analysis
```typescript
// Frontend API call
const correlation = await getCorrelationMatrix(["BTC", "ETH", "ADA"]);
```

```python
# Backend API call
POST /api/correlation
{
  "tickers": ["BTC", "ETH", "ADA"]
}
```

## 🔧 Configuration

### Backend Configuration
Edit `api.py`:
```python
# Change port
app.run(debug=True, port=5001)

# Disable debug mode for production
app.run(debug=False, port=5000)
```

### Frontend Configuration
Edit `asset-forecaster-pro-main/.env`:
```bash
# Development
VITE_API_URL=http://localhost:5000/api

# Production
VITE_API_URL=https://your-api-domain.com/api
```

## 🐛 Troubleshooting

### Backend Issues

**Port 5000 in use:**
```python
# Change port in api.py
app.run(debug=True, port=5001)
```

**Missing packages:**
```bash
pip install -r requirements.txt
```

**CORS errors:**
```bash
pip install flask-cors
```

### Frontend Issues

**API connection refused:**
- Ensure backend is running: `python api.py`
- Check `.env` file has correct URL

**Module not found:**
```bash
cd asset-forecaster-pro-main
npm install
```

**Port 5173 in use:**
- Vite will automatically use next available port

## 📈 Performance Notes

- **ARIMA:** ~2-3 seconds for 30-day forecast
- **Prophet:** ~3-5 seconds for 30-day forecast
- **LSTM:** ~5-10 seconds (30 epochs training)
- **Data Loading:** ~1-2 seconds for all cryptos
- **Correlation:** ~2-3 seconds for 10 cryptos

## 🔐 Security Considerations

### Development
- CORS allows all origins
- Debug mode enabled
- No authentication required

### Production
- [ ] Disable debug mode
- [ ] Configure specific CORS origins
- [ ] Add API authentication
- [ ] Implement rate limiting
- [ ] Use HTTPS
- [ ] Add input validation
- [ ] Set up logging

## 📦 Deployment

### Backend Deployment
```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api:app
```

### Frontend Deployment
```bash
cd asset-forecaster-pro-main

# Build for production
npm run build

# Deploy dist/ folder to:
# - Vercel
# - Netlify
# - AWS S3 + CloudFront
# - Any static hosting service
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📝 License

This project is for educational and research purposes.

## 🎉 Success Checklist

- [x] Backend API created and tested
- [x] Frontend integrated with API client
- [x] All endpoints working
- [x] Documentation complete
- [x] Startup scripts created
- [x] Verification script added
- [x] Test suite implemented
- [ ] Update frontend components to use real API
- [ ] Deploy to production
- [ ] Add authentication
- [ ] Implement caching

## 📞 Support

For issues or questions:
1. Run `python verify_setup.py`
2. Run `python test_api.py`
3. Check `INTEGRATION_GUIDE.md`
4. Check browser console for errors
5. Check Flask terminal for backend errors

## 🌟 Next Steps

1. **Update Frontend Components:**
   - Replace mock data with real API calls
   - Add loading states
   - Add error handling

2. **Enhance Features:**
   - Add more technical indicators
   - Implement portfolio tracking
   - Add price alerts
   - Export data to CSV

3. **Optimize Performance:**
   - Cache forecast results
   - Implement data pagination
   - Add request debouncing

4. **Production Ready:**
   - Add authentication
   - Implement rate limiting
   - Set up monitoring
   - Add logging

---

**Built with ❤️ using Python, Flask, React, and TypeScript**

🚀 **Ready to analyze crypto markets!**
