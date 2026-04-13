#!/usr/bin/env python3
"""
API Testing Script
Tests all backend endpoints to ensure they're working correctly
"""

import requests
import json
import time

API_BASE = "http://localhost:5000/api"

def print_test(name):
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print('='*60)

def test_health():
    print_test("Health Check")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data['status']}")
            print(f"✅ Cryptos loaded: {data['cryptos_loaded']}")
            return True
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection refused - Is the backend running?")
        print("   Run: python api.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_cryptos():
    print_test("GET /api/cryptos")
    try:
        response = requests.get(f"{API_BASE}/cryptos", timeout=5)
        if response.status_code == 200:
            cryptos = response.json()
            print(f"✅ Found {len(cryptos)} cryptocurrencies")
            print(f"   Sample: {', '.join([c['symbol'] for c in cryptos[:5]])}")
            return cryptos[0]['symbol'] if cryptos else None
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_get_data(ticker):
    print_test(f"GET /api/crypto/{ticker}/data")
    try:
        response = requests.get(f"{API_BASE}/crypto/{ticker}/data", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrieved {len(data)} data points")
            if data:
                latest = data[-1]
                print(f"   Latest: {latest['date']}")
                print(f"   Close: ${latest['close']:.2f}")
                print(f"   MA7: ${latest.get('ma7', 0):.2f}")
            return True
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_statistics(ticker):
    print_test(f"GET /api/crypto/{ticker}/statistics")
    try:
        response = requests.get(f"{API_BASE}/crypto/{ticker}/statistics", timeout=10)
        if response.status_code == 200:
            data = response.json()
            stats = data['price_statistics']
            vol = data['volatility_metrics']
            print(f"✅ Price Statistics:")
            print(f"   Current: ${stats['current']:.2f}")
            print(f"   Change: {stats['change_pct']:.2f}%")
            print(f"   Min: ${stats['min']:.2f}, Max: ${stats['max']:.2f}")
            print(f"✅ Volatility Metrics:")
            print(f"   Daily: {vol['daily_volatility']:.4f}")
            print(f"   Annual: {vol['annual_volatility']:.2f}")
            print(f"   Sharpe: {vol['sharpe_ratio']:.4f}")
            return True
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_technical(ticker):
    print_test(f"GET /api/crypto/{ticker}/technical")
    try:
        response = requests.get(f"{API_BASE}/crypto/{ticker}/technical", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Trend: {data['trend']}")
            print(f"✅ Volatility data points: {len(data['volatility'])}")
            print(f"✅ RSI data points: {len(data['rsi'])}")
            print(f"✅ Returns distribution bins: {len(data['returns_distribution'])}")
            stats = data['returns_stats']
            print(f"   Mean return: {stats['mean_return']:.4f}")
            print(f"   Positive days: {stats['positive_days']:.1f}%")
            return True
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_forecast(ticker):
    print_test(f"POST /api/forecast (ARIMA only)")
    try:
        payload = {
            "ticker": ticker,
            "days": 7,
            "models": ["arima"]
        }
        print("⏳ Training ARIMA model (this may take a few seconds)...")
        response = requests.post(f"{API_BASE}/forecast", json=payload, timeout=60)
        if response.status_code == 200:
            results = response.json()
            if results:
                model = results[0]
                print(f"✅ Model: {model['model']}")
                print(f"✅ Predictions: {len(model['predictions'])} days")
                if model['predictions']:
                    first = model['predictions'][0]
                    last = model['predictions'][-1]
                    print(f"   First: {first['date']} - ${first['price']:.2f}")
                    print(f"   Last: {last['date']} - ${last['price']:.2f}")
                return True
            else:
                print("❌ No forecast results returned")
                return False
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_correlation():
    print_test("POST /api/correlation")
    try:
        payload = {
            "tickers": ["BTC", "ETH", "ADA"]
        }
        response = requests.post(f"{API_BASE}/correlation", json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Tickers: {', '.join(data['tickers'])}")
            print(f"✅ Matrix size: {len(data['matrix'])}x{len(data['matrix'][0])}")
            print(f"   Sample correlations:")
            for i, ticker in enumerate(data['tickers'][:3]):
                print(f"   {ticker}: {data['matrix'][i][:3]}")
            return True
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "🧪 API TESTING SUITE".center(60))
    print("="*60)
    
    # Test health first
    if not test_health():
        print("\n❌ Backend is not running or not accessible")
        print("   Please start the backend: python api.py")
        return
    
    time.sleep(0.5)
    
    # Get a ticker to test with
    ticker = test_get_cryptos()
    if not ticker:
        print("\n❌ Could not get cryptocurrency list")
        return
    
    time.sleep(0.5)
    
    # Run all tests
    tests = [
        ("OHLC Data", lambda: test_get_data(ticker)),
        ("Statistics", lambda: test_get_statistics(ticker)),
        ("Technical Analysis", lambda: test_get_technical(ticker)),
        ("Forecasting", lambda: test_forecast(ticker)),
        ("Correlation", test_correlation),
    ]
    
    results = []
    for name, test_func in tests:
        time.sleep(0.5)
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Unexpected error in {name}: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY".center(60))
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results) + 1  # +1 for health check
    
    print(f"✅ Health Check")
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print("="*60)
    print(f"Results: {passed + 1}/{total} tests passed".center(60))
    print("="*60)
    
    if passed + 1 == total:
        print("\n🎉 All tests passed! API is working correctly.")
    else:
        print(f"\n⚠️  {total - passed - 1} test(s) failed. Check the output above.")
    
    print()

if __name__ == "__main__":
    main()
