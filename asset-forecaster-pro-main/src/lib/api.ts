import type {
  CryptoTicker,
  OHLCData,
  PriceStatistics,
  VolatilityMetrics,
  TechnicalData,
  ForecastResult,
  CorrelationMatrix,
} from "@/types/crypto";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";

export async function getCryptos(): Promise<CryptoTicker[]> {
  const response = await fetch(`${API_BASE_URL}/cryptos`);
  if (!response.ok) throw new Error("Failed to fetch cryptos");
  return response.json();
}

export async function getCryptoData(ticker: string): Promise<OHLCData[]> {
  const response = await fetch(`${API_BASE_URL}/crypto/${ticker}/data`);
  if (!response.ok) throw new Error(`Failed to fetch data for ${ticker}`);
  return response.json();
}

export async function getStatistics(ticker: string): Promise<{
  price_statistics: PriceStatistics;
  volatility_metrics: VolatilityMetrics;
}> {
  const response = await fetch(`${API_BASE_URL}/crypto/${ticker}/statistics`);
  if (!response.ok) throw new Error(`Failed to fetch statistics for ${ticker}`);
  return response.json();
}

export async function getTechnicalData(ticker: string): Promise<TechnicalData> {
  const response = await fetch(`${API_BASE_URL}/crypto/${ticker}/technical`);
  if (!response.ok) throw new Error(`Failed to fetch technical data for ${ticker}`);
  return response.json();
}

export async function generateForecast(
  ticker: string,
  days: number,
  models: string[]
): Promise<ForecastResult[]> {
  const response = await fetch(`${API_BASE_URL}/forecast`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ticker, days, models }),
  });
  if (!response.ok) throw new Error("Failed to generate forecast");
  return response.json();
}

export async function getCorrelationMatrix(tickers: string[]): Promise<CorrelationMatrix> {
  const response = await fetch(`${API_BASE_URL}/correlation`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tickers }),
  });
  if (!response.ok) throw new Error("Failed to fetch correlation matrix");
  return response.json();
}

export async function healthCheck(): Promise<{ status: string; cryptos_loaded: number }> {
  const response = await fetch(`${API_BASE_URL}/health`);
  if (!response.ok) throw new Error("Health check failed");
  return response.json();
}
