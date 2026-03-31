import pandas as pd  # library for data manipulation and analysis
import glob  # library to find files matching a pattern
import os  # library for operating system operations like file paths

class CryptoDataLoader:
    """load and preprocess cryptocurrency data from csv files"""
    
    def __init__(self, data_dir='.'):
        self.data_dir = data_dir  # store the directory where csv files are located
        self.data = {}  # empty dictionary to store loaded cryptocurrency data
        
    def load_all_cryptos(self):
        """load all cryptocurrency csv files from the directory"""
        # find all csv files in the data directory
        csv_files = glob.glob(os.path.join(self.data_dir, '*.csv'))
        
        # loop through each csv file found
        for file in csv_files:
            # extract ticker name from filename (e.g., 'BTC.csv' becomes 'BTC')
            ticker = os.path.basename(file).replace('.csv', '')
            try:
                df = pd.read_csv(file)  # read csv file into pandas dataframe
                df['date'] = pd.to_datetime(df['date'])  # convert date column to datetime format
                df = df.sort_values('date')  # sort data by date in ascending order
                df.set_index('date', inplace=True)  # set date as the index for time series analysis
                self.data[ticker] = df  # store the dataframe in dictionary with ticker as key
            except Exception as e:
                print(f"error loading {ticker}: {e}")  # print error if file loading fails
        
        return self.data  # return dictionary containing all loaded crypto data
    
    def load_single_crypto(self, ticker):
        """load a single cryptocurrency by ticker name"""
        # create full file path for the ticker
        file_path = os.path.join(self.data_dir, f'{ticker}.csv')
        if os.path.exists(file_path):  # check if file exists
            df = pd.read_csv(file_path)  # read the csv file
            df['date'] = pd.to_datetime(df['date'])  # convert date to datetime format
            df = df.sort_values('date')  # sort by date
            df.set_index('date', inplace=True)  # set date as index
            return df  # return the dataframe
        return None  # return none if file doesn't exist
    
    def get_available_tickers(self):
        """get list of available cryptocurrency tickers from csv files"""
        # find all csv files in directory
        csv_files = glob.glob(os.path.join(self.data_dir, '*.csv'))
        # extract ticker names from filenames and return sorted list
        return sorted([os.path.basename(f).replace('.csv', '') for f in csv_files])
