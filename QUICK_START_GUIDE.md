# Quick Start Guide
## Cryptocurrency Time Series Analysis Dashboard

### How to Run the Application

#### ✅ CORRECT WAY:
```bash
streamlit run app.py
```

#### ❌ WRONG WAY:
```bash
python app.py  # This will show warnings!
```

### Why?

Streamlit applications are web-based dashboards that need to be launched with the `streamlit run` command. Running `python app.py` directly will cause:
- "missing ScriptRunContext" warnings
- "Session state does not function" errors
- The app won't display properly in your browser

### Quick Launch Options

**Option 1: Command Line**
```bash
streamlit run app.py
```

**Option 2: Windows Batch File**
Double-click `run_app.bat` in the project folder

**Option 3: With Custom Port**
```bash
streamlit run app.py --server.port 8502
```

### What to Expect

1. The command will start a local web server
2. Your default browser will automatically open
3. The dashboard will load at `http://localhost:8501`
4. You'll see the cryptocurrency analysis interface

### Dashboard Features

1. **Overview Tab**
   - Current price and statistics
   - Price trend charts with moving averages
   - Candlestick charts
   - Statistical summaries

2. **Technical Analysis Tab**
   - Volatility analysis
   - Returns distribution
   - RSI indicator
   - Trend detection

3. **Forecasting Tab**
   - Select forecast period (7-90 days)
   - Choose models: ARIMA, Prophet, LSTM
   - Compare predictions
   - View forecast values

4. **Correlation Analysis Tab**
   - Select multiple cryptocurrencies
   - View correlation heatmap
   - Analyze relationships

### Troubleshooting

**Problem:** "streamlit: command not found"
**Solution:** Install streamlit first:
```bash
pip install -r requirements.txt
```

**Problem:** Port already in use
**Solution:** Use a different port:
```bash
streamlit run app.py --server.port 8502
```

**Problem:** Data not loading
**Solution:** Ensure CSV files are in the same directory as app.py

### Performance Tips

- LSTM training takes 1-2 minutes (30 epochs)
- Start with ARIMA and Prophet for faster results
- Reduce forecast days for quicker predictions
- Limit cryptocurrencies in correlation analysis

### System Requirements

- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended for LSTM)
- Modern web browser (Chrome, Firefox, Edge)
- Internet connection (for initial package installation)

### Need Help?

Contact: support@amdox.in
