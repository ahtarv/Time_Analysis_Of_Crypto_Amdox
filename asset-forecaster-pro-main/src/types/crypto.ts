export interface CryptoTicker {
  symbol: string;
  name: string;
}

export interface OHLCData {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  ma7?: number;
  ma30?: number;
  ma90?: number;
}

export interface PriceStatistics {
  mean: number;
  median: number;
  std: number;
  min: number;
  max: number;
  current: number;
  change_pct: number;
}

export interface VolatilityMetrics {
  daily_volatility: number;
  annual_volatility: number;
  sharpe_ratio: number;
}

export interface TechnicalData {
  trend: "Uptrend" | "Downtrend" | "Sideways";
  volatility: { date: string; value: number }[];
  returns_distribution: { bin: string; count: number }[];
  returns_stats: {
    mean_return: number;
    median_return: number;
    skewness: number;
    kurtosis: number;
    positive_days: number;
  };
  rsi: { date: string; value: number }[];
}

export interface ForecastResult {
  model: string;
  predictions: { date: string; price: number }[];
}

export interface CorrelationMatrix {
  tickers: string[];
  matrix: number[][];
}

export type TabType = "overview" | "technical" | "forecasting" | "correlation";
