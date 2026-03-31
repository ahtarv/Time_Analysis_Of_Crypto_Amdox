import pandas as pd  # library for data manipulation
import numpy as np  # library for numerical operations
from statsmodels.tsa.arima.model import ARIMA  # arima statistical model
from prophet import Prophet  # facebook's forecasting library
from sklearn.preprocessing import MinMaxScaler  # scale data to 0-1 range
from tensorflow.keras.models import Sequential  # neural network model
from tensorflow.keras.layers import LSTM, Dense, Dropout  # neural network layers
import warnings
warnings.filterwarnings('ignore')  # hide warning messages

class ARIMAForecaster:
    """arima (autoregressive integrated moving average) time series forecasting"""
    
    def __init__(self, order=(5, 1, 0)):
        # order = (p, d, q) where:
        # p = autoregressive terms (past values)
        # d = differencing order (make data stationary)
        # q = moving average terms (past errors)
        self.order = order
        self.model = None  # placeholder for trained model
        
    def fit(self, data):
        """train arima model on historical data"""
        self.model = ARIMA(data, order=self.order)  # create arima model
        self.model_fit = self.model.fit()  # train the model on data
        return self.model_fit
    
    def forecast(self, steps=30):
        """predict future prices for specified number of days"""
        if self.model_fit is None:
            raise ValueError("model not fitted yet")  # check if model is trained
        forecast = self.model_fit.forecast(steps=steps)  # generate predictions
        return forecast

class ProphetForecaster:
    """facebook prophet forecasting (handles seasonality well)"""
    
    def __init__(self):
        # create prophet model with daily and yearly patterns
        self.model = Prophet(daily_seasonality=True, yearly_seasonality=True)
        
    def fit(self, df, column='close'):
        """train prophet model on historical data"""
        prophet_df = df.reset_index()  # reset index to get date as column
        # prophet requires columns named 'ds' (date) and 'y' (value)
        prophet_df = prophet_df.rename(columns={'date': 'ds', column: 'y'})
        self.model.fit(prophet_df[['ds', 'y']])  # train model
        return self.model
    
    def forecast(self, periods=30):
        """predict future prices for specified number of days"""
        # create future dates dataframe
        future = self.model.make_future_dataframe(periods=periods)
        forecast = self.model.predict(future)  # generate predictions
        return forecast

class LSTMForecaster:
    """lstm (long short-term memory) neural network forecasting"""
    
    def __init__(self, lookback=60, units=50):
        self.lookback = lookback  # number of past days to use for prediction
        self.units = units  # number of neurons in lstm layers
        self.model = None  # placeholder for neural network
        # scaler to normalize data between 0 and 1 (helps neural network learn)
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        
    def prepare_data(self, data):
        """prepare data for lstm neural network training"""
        # scale data to 0-1 range (neural networks work better with normalized data)
        scaled_data = self.scaler.fit_transform(data.values.reshape(-1, 1))
        
        X, y = [], []  # input features and target values
        # create sequences: use past 60 days to predict next day
        for i in range(self.lookback, len(scaled_data)):
            X.append(scaled_data[i-self.lookback:i, 0])  # past 60 days
            y.append(scaled_data[i, 0])  # next day to predict
        
        X, y = np.array(X), np.array(y)  # convert to numpy arrays
        # reshape for lstm: (samples, time steps, features)
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))
        
        return X, y
    
    def build_model(self, input_shape):
        """build lstm neural network architecture"""
        model = Sequential([  # sequential model (layers stacked one after another)
            # first lstm layer with 50 neurons, returns sequences for next layer
            LSTM(units=self.units, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),  # dropout 20% neurons to prevent overfitting
            # second lstm layer with 50 neurons
            LSTM(units=self.units, return_sequences=False),
            Dropout(0.2),  # dropout again
            Dense(units=25),  # fully connected layer with 25 neurons
            Dense(units=1)  # output layer with 1 neuron (predicted price)
        ])
        # compile model with adam optimizer and mse loss function
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model
    
    def fit(self, data, epochs=50, batch_size=32):
        """train lstm neural network on historical data"""
        X, y = self.prepare_data(data)  # prepare training data
        self.model = self.build_model((X.shape[1], 1))  # build network architecture
        # train model for 50 epochs with batch size of 32
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=0)
        return self.model
    
    def forecast(self, data, steps=30):
        """predict future prices using trained lstm model"""
        # scale the data using same scaler from training
        scaled_data = self.scaler.transform(data.values.reshape(-1, 1))
        predictions = []  # store predictions
        
        # start with last 60 days of actual data
        current_batch = scaled_data[-self.lookback:].reshape(1, self.lookback, 1)
        
        # predict one day at a time for specified steps
        for _ in range(steps):
            pred = self.model.predict(current_batch, verbose=0)[0]  # predict next day
            predictions.append(pred)  # store prediction
            # update batch: remove oldest day, add new prediction
            current_batch = np.append(current_batch[:, 1:, :], [[pred]], axis=1)
        
        # convert predictions back to original price scale
        predictions = self.scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
        return predictions.flatten()  # return as 1d array
