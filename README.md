# Cryptocurrency Time Series Analysis & Forecasting

A comprehensive data analytics project for analyzing cryptocurrency price trends using time series forecasting techniques including ARIMA, LSTM, and Facebook Prophet.

## Features

- **Data Collection & Preprocessing**: Automated loading of 100+ cryptocurrency CSV files
- **Exploratory Data Analysis**: Statistical analysis, trend detection, volatility metrics
- **Technical Indicators**: Moving averages, RSI, volatility analysis
- **Time Series Forecasting**: ARIMA, LSTM, and Prophet models
- **Interactive Dashboard**: Streamlit-based GUI with real-time visualizations
- **Correlation Analysis**: Multi-cryptocurrency correlation heatmaps
- **Visualization**: Candlestick charts, price trends, returns distribution

## Installation

1. Install Python 3.8 or higher

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Run the Streamlit Dashboard

**IMPORTANT:** Use the correct command to launch the app:

```bash
streamlit run app.py
```

**DO NOT** run `python app.py` directly - this will cause warnings. Streamlit apps must be launched with the `streamlit run` command.

Alternatively, on Windows, double-click `run_app.bat` to start the dashboard.

The dashboard will open in your browser at `http://localhost:8501`

### Quick Analysis Script

```python
from data_loader import CryptoDataLoader
from data_preprocessing import DataPreprocessor
from analysis import CryptoAnalyzer

# Load data
loader = CryptoDataLoader('.')
data = loader.load_all_cryptos()

# Analyze Bitcoin
btc_df = data['BTC']
preprocessor = DataPreprocessor()
btc_df = preprocessor.calculate_returns(btc_df)
btc_df = preprocessor.calculate_moving_averages(btc_df)

# Get statistics
analyzer = CryptoAnalyzer()
stats = analyzer.calculate_statistics(btc_df)
print(stats)
```

## Project Structure

```
.
├── app.py                      # Main Streamlit dashboard
├── data_loader.py              # Data loading utilities
├── data_preprocessing.py       # Data preprocessing & feature engineering
├── analysis.py                 # Statistical analysis functions
├── forecasting_models.py       # ARIMA, LSTM, Prophet models
├── visualization.py            # Plotly visualization functions
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── *.csv                       # Cryptocurrency data files
```

## Models

### ARIMA (AutoRegressive Integrated Moving Average)
- Statistical model for time series forecasting
- Best for short-term predictions
- Captures linear trends and seasonality

### LSTM (Long Short-Term Memory)
- Deep learning neural network
- Captures complex non-linear patterns
- Requires more data and computational resources

### Prophet
- Facebook's forecasting tool
- Handles missing data and outliers well
- Good for data with strong seasonal patterns

## Dashboard Sections

1. **Overview**: Key metrics, price trends, candlestick charts
2. **Technical Analysis**: Volatility, returns distribution, RSI indicator
3. **Forecasting**: Multi-model price predictions with comparison
4. **Correlation Analysis**: Cross-cryptocurrency correlation heatmaps

## Data Format

CSV files should have the following columns:
- `ticker`: Cryptocurrency symbol
- `date`: Date in YYYY-MM-DD format
- `open`: Opening price
- `high`: Highest price
- `low`: Lowest price
- `close`: Closing price

## Performance Tips

- For faster LSTM training, reduce epochs (default: 30)
- Use fewer cryptocurrencies for correlation analysis
- Limit forecast days for quicker results

## Requirements

- Python 3.8+
- pandas
- numpy
- matplotlib
- seaborn
- plotly
- streamlit
- scikit-learn
- statsmodels
- prophet
- tensorflow

## License

This project is for educational purposes.

## Contact

support@amdox.in
