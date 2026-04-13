# 🏗️ System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER BROWSER                         │
│                    http://localhost:5173                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ HTTP/REST API
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    REACT FRONTEND                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Components (Dashboard, Charts, Tables)                │ │
│  └────────────────────────┬───────────────────────────────┘ │
│  ┌────────────────────────▼───────────────────────────────┐ │
│  │  API Client (lib/api.ts)                               │ │
│  │  - getCryptos()                                        │ │
│  │  - getCryptoData()                                     │ │
│  │  - getStatistics()                                     │ │
│  │  - getTechnicalData()                                  │ │
│  │  - generateForecast()                                  │ │
│  │  - getCorrelationMatrix()                              │ │
│  └────────────────────────┬───────────────────────────────┘ │
└───────────────────────────┼─────────────────────────────────┘
                            │
                            │ fetch() requests
                            │ JSON responses
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    FLASK REST API                            │
│                  http://localhost:5000                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Endpoints (api.py)                                    │ │
│  │  GET  /api/cryptos                                     │ │
│  │  GET  /api/crypto/<ticker>/data                        │ │
│  │  GET  /api/crypto/<ticker>/statistics                  │ │
│  │  GET  /api/crypto/<ticker>/technical                   │ │
│  │  POST /api/forecast                                    │ │
│  │  POST /api/correlation                                 │ │
│  │  GET  /api/health                                      │ │
│  └────────────────────────┬───────────────────────────────┘ │
└───────────────────────────┼─────────────────────────────────┘
                            │
                            │ Python function calls
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    PYTHON BACKEND MODULES                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  CryptoDataLoader (data_loader.py)                     │ │
│  │  - load_all_cryptos()                                  │ │
│  │  - get_available_tickers()                             │ │
│  └────────────────────────┬───────────────────────────────┘ │
│  ┌────────────────────────▼───────────────────────────────┐ │
│  │  DataPreprocessor (data_preprocessing.py)              │ │
│  │  - handle_missing_values()                             │ │
│  │  - calculate_returns()                                 │ │
│  │  - calculate_moving_averages()                         │ │
│  │  - calculate_rsi()                                     │ │
│  └────────────────────────┬───────────────────────────────┘ │
│  ┌────────────────────────▼───────────────────────────────┐ │
│  │  CryptoAnalyzer (analysis.py)                          │ │
│  │  - calculate_statistics()                              │ │
│  │  - calculate_volatility_metrics()                      │ │
│  │  - detect_trend()                                      │ │
│  │  - calculate_correlation_matrix()                      │ │
│  └────────────────────────┬───────────────────────────────┘ │
│  ┌────────────────────────▼───────────────────────────────┐ │
│  │  Forecasting Models (forecasting_models.py)            │ │
│  │  - ARIMAForecaster                                     │ │
│  │  - ProphetForecaster                                   │ │
│  │  - LSTMForecaster                                      │ │
│  └────────────────────────┬───────────────────────────────┘ │
└───────────────────────────┼─────────────────────────────────┘
                            │
                            │ File I/O
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    DATA STORAGE (CSV FILES)                  │
│  BTC.csv, ETH.csv, ADA.csv, SOL.csv, ...                   │
│  Columns: date, open, high, low, close, volume              │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

### Example: Generate Forecast

```
1. User Action
   └─> User clicks "Generate Forecast" button
       └─> Selects: BTC, 30 days, [ARIMA, Prophet]

2. Frontend Processing
   └─> React component calls generateForecast()
       └─> API client sends POST request
           └─> URL: http://localhost:5000/api/forecast
           └─> Body: {"ticker": "BTC", "days": 30, "models": ["arima", "prophet"]}

3. Backend API Layer
   └─> Flask receives POST /api/forecast
       └─> Extracts: ticker, days, models from request.json
       └─> Validates input parameters

4. Data Loading
   └─> CryptoDataLoader.load_all_cryptos()
       └─> Reads BTC.csv from disk
       └─> Returns pandas DataFrame

5. Data Preprocessing
   └─> DataPreprocessor.handle_missing_values()
       └─> DataPreprocessor.prepare_for_modeling()
       └─> Returns clean DataFrame

6. Model Training & Forecasting
   └─> For each model in ["arima", "prophet"]:
       
       ARIMA:
       └─> ARIMAForecaster()
           └─> fit(historical_data)
               └─> ARIMA(order=(10,1,2))
           └─> forecast(steps=30)
               └─> Returns 30-day predictions
       
       Prophet:
       └─> ProphetForecaster()
           └─> fit(historical_data)
               └─> Prophet model training
           └─> forecast(periods=30)
               └─> Returns 30-day predictions

7. Response Formatting
   └─> Format predictions as JSON
       └─> [
             {"model": "ARIMA", "predictions": [...]},
             {"model": "Prophet", "predictions": [...]}
           ]

8. API Response
   └─> Flask returns JSON response
       └─> Status: 200 OK
       └─> Content-Type: application/json

9. Frontend Update
   └─> React receives forecast data
       └─> Updates component state
       └─> Recharts renders forecast chart
       └─> User sees predictions visualized
```

## Component Architecture

### Frontend Components

```
App.tsx
├── QueryClientProvider (React Query)
├── BrowserRouter (React Router)
└── Routes
    ├── Index.tsx (Main Dashboard)
    │   ├── Header
    │   ├── CryptoSelector
    │   ├── TabNavigation
    │   └── TabContent
    │       ├── OverviewTab
    │       │   ├── MetricCards
    │       │   ├── PriceChart
    │       │   ├── CandlestickChart
    │       │   └── StatisticsTables
    │       ├── TechnicalTab
    │       │   ├── TrendIndicator
    │       │   ├── VolatilityChart
    │       │   ├── ReturnsHistogram
    │       │   └── RSIChart
    │       ├── ForecastingTab
    │       │   ├── ForecastControls
    │       │   ├── ModelSelector
    │       │   ├── ForecastChart
    │       │   └── ForecastTable
    │       └── CorrelationTab
    │           ├── CryptoMultiSelect
    │           ├── CorrelationHeatmap
    │           └── CorrelationMatrix
    └── NotFound.tsx
```

### Backend Modules

```
api.py (Flask App)
├── CORS Configuration
├── Route Handlers
│   ├── /api/health
│   ├── /api/cryptos
│   ├── /api/crypto/<ticker>/data
│   ├── /api/crypto/<ticker>/statistics
│   ├── /api/crypto/<ticker>/technical
│   ├── /api/forecast
│   └── /api/correlation
└── Error Handlers

data_loader.py
└── CryptoDataLoader
    ├── __init__(data_dir)
    ├── load_all_cryptos()
    ├── load_single_crypto(ticker)
    └── get_available_tickers()

data_preprocessing.py
└── DataPreprocessor
    ├── handle_missing_values(df)
    ├── calculate_returns(df)
    ├── calculate_log_returns(df)
    ├── calculate_volatility(df)
    ├── calculate_moving_averages(df)
    ├── calculate_rsi(df)
    └── prepare_for_modeling(df)

analysis.py
└── CryptoAnalyzer
    ├── calculate_statistics(df)
    ├── calculate_volatility_metrics(df)
    ├── detect_trend(df)
    ├── calculate_correlation_matrix(data_dict)
    └── calculate_returns_distribution(df)

forecasting_models.py
├── ARIMAForecaster
│   ├── __init__(order)
│   ├── fit(data)
│   └── forecast(steps)
├── ProphetForecaster
│   ├── __init__()
│   ├── fit(df)
│   └── forecast(periods)
└── LSTMForecaster
    ├── __init__(lookback, units)
    ├── prepare_data(data)
    ├── build_model(input_shape)
    ├── fit(data, epochs)
    └── forecast(data, steps)
```

## Technology Stack Layers

```
┌─────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                      │
│  React Components, Tailwind CSS, shadcn/ui, Recharts        │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                      APPLICATION LAYER                       │
│  React Hooks, State Management, React Query, React Router   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                      API CLIENT LAYER                        │
│  TypeScript API Client, fetch(), Error Handling             │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ HTTP/REST
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                      API GATEWAY LAYER                       │
│  Flask REST API, CORS, Request Validation, JSON Responses   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                      BUSINESS LOGIC LAYER                    │
│  Analysis, Preprocessing, Forecasting, Calculations         │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                      DATA ACCESS LAYER                       │
│  Data Loading, CSV Parsing, DataFrame Operations            │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                      DATA STORAGE LAYER                      │
│  CSV Files (BTC.csv, ETH.csv, etc.)                         │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Architecture

### Development Environment

```
Developer Machine
├── Backend (Port 5000)
│   └── python api.py
└── Frontend (Port 5173)
    └── npm run dev
```

### Production Environment

```
                    ┌─────────────────┐
                    │   Users/Clients │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   Load Balancer │
                    │   (HTTPS/SSL)   │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
     ┌────────▼────────┐         ┌─────────▼────────┐
     │  Frontend CDN   │         │  Backend Servers │
     │  (Static Files) │         │  (Flask + WSGI)  │
     │  Vercel/Netlify │         │  Gunicorn/uWSGI  │
     └─────────────────┘         └─────────┬────────┘
                                           │
                                  ┌────────▼────────┐
                                  │  Data Storage   │
                                  │  (CSV/Database) │
                                  └─────────────────┘
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         SECURITY LAYERS                      │
├─────────────────────────────────────────────────────────────┤
│  1. Transport Layer                                          │
│     └─> HTTPS/TLS encryption                                │
├─────────────────────────────────────────────────────────────┤
│  2. Authentication Layer                                     │
│     └─> API Keys / JWT Tokens (to be implemented)           │
├─────────────────────────────────────────────────────────────┤
│  3. Authorization Layer                                      │
│     └─> Role-based access control (to be implemented)       │
├─────────────────────────────────────────────────────────────┤
│  4. Input Validation Layer                                   │
│     └─> Request validation, sanitization                    │
├─────────────────────────────────────────────────────────────┤
│  5. CORS Layer                                               │
│     └─> Cross-origin resource sharing policies              │
├─────────────────────────────────────────────────────────────┤
│  6. Rate Limiting Layer                                      │
│     └─> Request throttling (to be implemented)              │
└─────────────────────────────────────────────────────────────┘
```

## Performance Optimization

### Caching Strategy

```
Request Flow with Caching:

User Request
    │
    ├─> Check Browser Cache (React Query)
    │   └─> Hit? Return cached data
    │   └─> Miss? Continue...
    │
    ├─> API Request to Backend
    │   │
    │   ├─> Check Server Cache (Redis/Memcached)
    │   │   └─> Hit? Return cached data
    │   │   └─> Miss? Continue...
    │   │
    │   └─> Process Request
    │       └─> Cache Result
    │       └─> Return Response
    │
    └─> Cache in Browser
        └─> Display to User
```

## Monitoring & Logging

```
┌─────────────────────────────────────────────────────────────┐
│                      MONITORING STACK                        │
├─────────────────────────────────────────────────────────────┤
│  Frontend Monitoring                                         │
│  └─> Error tracking (Sentry)                                │
│  └─> Performance monitoring (Web Vitals)                    │
│  └─> User analytics (Google Analytics)                      │
├─────────────────────────────────────────────────────────────┤
│  Backend Monitoring                                          │
│  └─> Application logs (Python logging)                      │
│  └─> API metrics (request count, latency)                   │
│  └─> Error tracking (Sentry)                                │
│  └─> Health checks (/api/health)                            │
├─────────────────────────────────────────────────────────────┤
│  Infrastructure Monitoring                                   │
│  └─> Server metrics (CPU, memory, disk)                     │
│  └─> Network metrics (bandwidth, latency)                   │
│  └─> Uptime monitoring                                      │
└─────────────────────────────────────────────────────────────┘
```

---

This architecture provides:
- ✅ Clear separation of concerns
- ✅ Scalable design
- ✅ Easy to maintain and extend
- ✅ Production-ready structure
- ✅ Security considerations
- ✅ Performance optimization paths
