import streamlit as st  # web app framework for creating dashboard
import pandas as pd  # data manipulation library
import numpy as np  # numerical operations library
from datetime import datetime, timedelta  # date and time operations
from data_loader import CryptoDataLoader  # our custom data loading class
from data_preprocessing import DataPreprocessor  # our custom preprocessing class
from analysis import CryptoAnalyzer  # our custom analysis class
from forecasting_models import ARIMAForecaster, ProphetForecaster, LSTMForecaster  # forecasting models
from visualization import CryptoVisualizer  # our custom visualization class
import warnings
warnings.filterwarnings('ignore')  # hide warning messages

# configure streamlit page settings
st.set_page_config(page_title="crypto time series analysis", layout="wide", page_icon="📈")

# display main title
st.title("📈 cryptocurrency time series analysis & forecasting")
st.markdown("---")  # horizontal line separator

# initialize components
@st.cache_resource  # cache data so it loads only once (faster performance)
def load_data():
    """load all cryptocurrency data from csv files"""
    loader = CryptoDataLoader('.')  # create loader for current directory
    return loader.load_all_cryptos(), loader.get_available_tickers()

# load data with loading spinner
with st.spinner("loading cryptocurrency data..."):
    crypto_data, available_tickers = load_data()  # load all crypto data

# sidebar configuration panel
st.sidebar.header("⚙️ configuration")
# dropdown to select which cryptocurrency to analyze
selected_ticker = st.sidebar.selectbox("select cryptocurrency", available_tickers)
# radio buttons to choose analysis type
analysis_type = st.sidebar.radio("analysis type", 
                                 ["overview", "technical analysis", "forecasting", "correlation analysis"])

# get selected crypto data
if selected_ticker in crypto_data:
    df = crypto_data[selected_ticker].copy()  # get dataframe for selected crypto
    
    # preprocess data (clean and calculate indicators)
    preprocessor = DataPreprocessor()
    df = preprocessor.handle_missing_values(df)  # fill missing values
    df = preprocessor.calculate_returns(df)  # calculate daily returns
    df = preprocessor.calculate_log_returns(df)  # calculate log returns
    df = preprocessor.calculate_volatility(df)  # calculate volatility
    df = preprocessor.calculate_moving_averages(df)  # calculate moving averages
    df = preprocessor.calculate_rsi(df)  # calculate rsi indicator
    
    analyzer = CryptoAnalyzer()  # create analyzer object
    visualizer = CryptoVisualizer()  # create visualizer object
    
    # overview tab - shows basic statistics and price charts
    if analysis_type == "overview":
        st.header(f"📊 {selected_ticker} overview")
        
        # display key metrics in 4 columns
        col1, col2, col3, col4 = st.columns(4)
        stats = analyzer.calculate_statistics(df)  # get statistics
        
        # display metrics in separate columns
        with col1:
            st.metric("current price", f"${stats['current']:.2f}")
        with col2:
            st.metric("change %", f"{stats['change_pct']:.2f}%")
        with col3:
            st.metric("max price", f"${stats['max']:.2f}")
        with col4:
            st.metric("min price", f"${stats['min']:.2f}")
        
        # price trend chart with moving averages
        st.subheader("price trend")
        fig_price = visualizer.plot_price_trend(df, selected_ticker)
        st.plotly_chart(fig_price, width='stretch')  # display chart
        
        # candlestick chart for last 90 days
        st.subheader("candlestick chart (last 90 days)")
        fig_candle = visualizer.plot_candlestick(df.tail(90), selected_ticker)
        st.plotly_chart(fig_candle, width='stretch')
        
        # statistics tables in two columns
        st.subheader("statistical summary")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**price statistics**")
            # display statistics as table
            st.dataframe(pd.DataFrame([stats]).T, width='stretch')
        
        with col2:
            vol_metrics = analyzer.calculate_volatility_metrics(df)
            st.write("**volatility metrics**")
            st.dataframe(pd.DataFrame([vol_metrics]).T, width='stretch')
    
    # technical analysis tab - shows volatility, returns, rsi
    elif analysis_type == "technical analysis":
        st.header(f"🔍 {selected_ticker} technical analysis")
        
        # detect and display current trend
        trend = analyzer.detect_trend(df)
        st.info(f"**current trend:** {trend}")
        
        # volatility chart shows risk over time
        st.subheader("volatility analysis")
        fig_vol = visualizer.plot_volatility(df, selected_ticker)
        st.plotly_chart(fig_vol, width='stretch')
        
        # returns distribution histogram
        st.subheader("returns distribution")
        fig_returns = visualizer.plot_returns_distribution(df)
        st.plotly_chart(fig_returns, width='stretch')
        
        # returns statistics table
        returns_stats = analyzer.calculate_returns_distribution(df)
        st.write("**returns statistics**")
        st.dataframe(pd.DataFrame([returns_stats]).T, width='stretch')
        
        # rsi indicator chart (overbought/oversold indicator)
        st.subheader("rsi indicator")
        st.line_chart(df['RSI'].tail(90))  # show last 90 days
        
    # forecasting tab - predict future prices using ml models
    elif analysis_type == "forecasting":
        st.header(f"🔮 {selected_ticker} price forecasting")
        
        # slider to choose how many days to forecast
        forecast_days = st.sidebar.slider("forecast days", 7, 90, 30)
        # multiselect to choose which models to use
        model_choice = st.sidebar.multiselect("select models", 
                                              ["arima", "prophet", "lstm"],
                                              default=["arima", "prophet"])
        
        # button to start forecasting
        if st.sidebar.button("generate forecast"):
            with st.spinner("training models and generating forecasts..."):
                forecasts = {}  # store forecasts from different models
                df_clean = preprocessor.prepare_for_modeling(df)  # prepare clean data
                
                # arima model forecasting
                if "arima" in model_choice:
                    try:
                        arima = ARIMAForecaster()  # create arima model
                        arima.fit(df_clean['close'])  # train on historical data
                        arima_forecast = arima.forecast(steps=forecast_days)  # predict
                        # create future dates for predictions
                        forecast_dates = pd.date_range(start=df.index[-1] + timedelta(days=1), 
                                                      periods=forecast_days, freq='D')
                        forecasts['arima'] = {'dates': forecast_dates, 'values': arima_forecast}
                        st.success("✅ arima model completed")
                    except Exception as e:
                        st.error(f"arima error: {e}")
                
                # prophet model forecasting
                if "prophet" in model_choice:
                    try:
                        prophet = ProphetForecaster()  # create prophet model
                        prophet.fit(df_clean)  # train on historical data
                        prophet_forecast = prophet.forecast(periods=forecast_days)  # predict
                        forecasts['prophet'] = {
                            'dates': prophet_forecast['ds'].tail(forecast_days),
                            'values': prophet_forecast['yhat'].tail(forecast_days)
                        }
                        st.success("✅ prophet model completed")
                    except Exception as e:
                        st.error(f"prophet error: {e}")
                
                # lstm neural network forecasting
                if "lstm" in model_choice:
                    try:
                        lstm = LSTMForecaster(lookback=60)  # create lstm model
                        lstm.fit(df_clean['close'], epochs=30)  # train neural network
                        lstm_forecast = lstm.forecast(df_clean['close'], steps=forecast_days)
                        forecast_dates = pd.date_range(start=df.index[-1] + timedelta(days=1), 
                                                      periods=forecast_days, freq='D')
                        forecasts['lstm'] = {'dates': forecast_dates, 'values': lstm_forecast}
                        st.success("✅ lstm model completed")
                    except Exception as e:
                        st.error(f"lstm error: {e}")
                
                # plot all forecasts together for comparison
                if forecasts:
                    fig_forecast = visualizer.plot_forecast_comparison(df.tail(90), forecasts, selected_ticker)
                    st.plotly_chart(fig_forecast, width='stretch')
                    
                    # display forecast values in table
                    st.subheader("forecast values")
                    forecast_df = pd.DataFrame({
                        model: data['values'] for model, data in forecasts.items()
                    })
                    forecast_df.index = list(forecasts.values())[0]['dates']
                    st.dataframe(forecast_df, width='stretch')
    
    # correlation analysis tab - shows how cryptos move together
    elif analysis_type == "correlation analysis":
        st.header("🔗 cryptocurrency correlation analysis")
        
        # multiselect to choose which cryptos to compare
        selected_cryptos = st.multiselect("select cryptocurrencies (max 20)", 
                                         available_tickers, 
                                         default=available_tickers[:10])
        
        if len(selected_cryptos) >= 2:  # need at least 2 cryptos for correlation
            # filter data for selected cryptos only
            filtered_data = {ticker: crypto_data[ticker] for ticker in selected_cryptos if ticker in crypto_data}
            # calculate correlation matrix
            corr_matrix = analyzer.calculate_correlation_matrix(filtered_data)
            
            # display correlation heatmap
            fig_corr = visualizer.plot_correlation_heatmap(corr_matrix)
            st.plotly_chart(fig_corr, width='stretch')
            
            # display correlation values in table with color gradient
            st.subheader("correlation matrix")
            st.dataframe(corr_matrix.style.background_gradient(cmap='RdBu', vmin=-1, vmax=1),
                        width='stretch')
        else:
            st.warning("please select at least 2 cryptocurrencies for correlation analysis")

else:
    st.error(f"data for {selected_ticker} not found")  # error if crypto not found

# footer
st.markdown("---")
st.markdown("**data analytics project** | time series analysis with cryptocurrency")
