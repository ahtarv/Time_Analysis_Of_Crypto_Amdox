"""
quick analysis script to analyze all cryptocurrencies at once
run this for a fast overview of all 100 cryptos
"""

import pandas as pd  # data manipulation library
from data_loader import CryptoDataLoader  # our custom data loader
from data_preprocessing import DataPreprocessor  # our custom preprocessor
from analysis import CryptoAnalyzer  # our custom analyzer
import warnings
warnings.filterwarnings('ignore')  # hide warning messages

def analyze_all_cryptos():
    """analyze all cryptocurrencies and generate summary report"""
    
    print("loading cryptocurrency data...")
    loader = CryptoDataLoader('.')  # create loader for current directory
    data = loader.load_all_cryptos()  # load all csv files
    
    print(f"loaded {len(data)} cryptocurrencies\n")
    
    preprocessor = DataPreprocessor()  # create preprocessor
    analyzer = CryptoAnalyzer()  # create analyzer
    
    results = []  # list to store analysis results
    
    # loop through each cryptocurrency
    for ticker, df in data.items():
        try:
            # preprocess data
            df = preprocessor.handle_missing_values(df)  # fill missing values
            df = preprocessor.calculate_returns(df)  # calculate returns
            df = preprocessor.calculate_volatility(df)  # calculate volatility
            
            # analyze data
            stats = analyzer.calculate_statistics(df)  # get price statistics
            vol_metrics = analyzer.calculate_volatility_metrics(df)  # get volatility metrics
            trend = analyzer.detect_trend(df)  # detect trend direction
            
            # store results in dictionary
            results.append({
                'ticker': ticker,
                'current price': f"${stats['current']:.2f}",
                'change %': f"{stats['change_pct']:.2f}%",
                'volatility': f"{vol_metrics['annual_volatility']:.2%}",
                'sharpe ratio': f"{vol_metrics['sharpe_ratio']:.2f}",
                'trend': trend,
                'min price': f"${stats['min']:.2f}",
                'max price': f"${stats['max']:.2f}"
            })
            
        except Exception as e:
            print(f"error analyzing {ticker}: {e}")
    
    # create summary dataframe from results
    summary_df = pd.DataFrame(results)
    
    # sort by change percentage (best performers first)
    summary_df['change_numeric'] = summary_df['change %'].str.rstrip('%').astype(float)
    summary_df = summary_df.sort_values('change_numeric', ascending=False)
    summary_df = summary_df.drop('change_numeric', axis=1)  # remove helper column
    
    # display results
    print("\n" + "="*100)
    print("cryptocurrency analysis summary")
    print("="*100 + "\n")
    
    print(summary_df.to_string(index=False))  # print full table
    
    # save to csv file
    summary_df.to_csv('crypto_analysis_summary.csv', index=False)
    print(f"\n✅ summary saved to 'crypto_analysis_summary.csv'")
    
    # show top 10 performers (highest gains)
    print("\n" + "="*100)
    print("top 10 performers")
    print("="*100)
    print(summary_df.head(10).to_string(index=False))
    
    # show bottom 10 performers (biggest losses)
    print("\n" + "="*100)
    print("bottom 10 performers")
    print("="*100)
    print(summary_df.tail(10).to_string(index=False))
    
    return summary_df

# run analysis when script is executed directly
if __name__ == "__main__":
    summary = analyze_all_cryptos()
