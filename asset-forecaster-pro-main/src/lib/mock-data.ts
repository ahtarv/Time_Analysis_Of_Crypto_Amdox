import type {
  CryptoTicker,
  OHLCData,
  PriceStatistics,
  VolatilityMetrics,
  TechnicalData,
  ForecastResult,
  CorrelationMatrix,
} from "@/types/crypto";

const CRYPTOS: CryptoTicker[] = [
  { symbol: "BTC", name: "Bitcoin" },
  { symbol: "ETH", name: "Ethereum" },
  { symbol: "ADA", name: "Cardano" },
  { symbol: "SOL", name: "Solana" },
  { symbol: "DOT", name: "Polkadot" },
  { symbol: "AVAX", name: "Avalanche" },
  { symbol: "MATIC", name: "Polygon" },
  { symbol: "LINK", name: "Chainlink" },
  { symbol: "UNI", name: "Uniswap" },
  { symbol: "ATOM", name: "Cosmos" },
  { symbol: "XRP", name: "Ripple" },
  { symbol: "DOGE", name: "Dogecoin" },
  { symbol: "SHIB", name: "Shiba Inu" },
  { symbol: "LTC", name: "Litecoin" },
  { symbol: "BCH", name: "Bitcoin Cash" },
  { symbol: "ALGO", name: "Algorand" },
  { symbol: "FTM", name: "Fantom" },
  { symbol: "NEAR", name: "NEAR Protocol" },
  { symbol: "AAVE", name: "Aave" },
  { symbol: "CRV", name: "Curve" },
];

const basePrices: Record<string, number> = {
  BTC: 67500, ETH: 3450, ADA: 0.62, SOL: 148, DOT: 7.8,
  AVAX: 38, MATIC: 0.72, LINK: 15.5, UNI: 8.2, ATOM: 9.5,
  XRP: 0.58, DOGE: 0.12, SHIB: 0.000025, LTC: 85, BCH: 480,
  ALGO: 0.22, FTM: 0.45, NEAR: 5.8, AAVE: 95, CRV: 0.55,
};

function seededRandom(seed: number): () => number {
  let s = seed;
  return () => {
    s = (s * 16807) % 2147483647;
    return (s - 1) / 2147483646;
  };
}

export function getCryptos(): CryptoTicker[] {
  return CRYPTOS;
}

export function generateOHLCData(ticker: string, days = 180): OHLCData[] {
  const base = basePrices[ticker] || 100;
  const rand = seededRandom(ticker.charCodeAt(0) * 137);
  const data: OHLCData[] = [];
  let price = base * (0.8 + rand() * 0.4);

  for (let i = days; i >= 0; i--) {
    const date = new Date();
    date.setDate(date.getDate() - i);
    const volatility = 0.02 + rand() * 0.03;
    const change = (rand() - 0.48) * volatility;
    price = price * (1 + change);
    const high = price * (1 + rand() * 0.02);
    const low = price * (1 - rand() * 0.02);
    const open = price * (1 + (rand() - 0.5) * 0.015);

    data.push({
      date: date.toISOString().split("T")[0],
      open: +open.toFixed(6),
      high: +high.toFixed(6),
      low: +low.toFixed(6),
      close: +price.toFixed(6),
      volume: Math.floor(rand() * 1e9),
    });
  }

  // Calculate moving averages
  for (let i = 0; i < data.length; i++) {
    if (i >= 6) data[i].ma7 = +( data.slice(i - 6, i + 1).reduce((s, d) => s + d.close, 0) / 7).toFixed(6);
    if (i >= 29) data[i].ma30 = +(data.slice(i - 29, i + 1).reduce((s, d) => s + d.close, 0) / 30).toFixed(6);
    if (i >= 89) data[i].ma90 = +(data.slice(i - 89, i + 1).reduce((s, d) => s + d.close, 0) / 90).toFixed(6);
  }

  return data;
}

export function getStatistics(data: OHLCData[]): PriceStatistics {
  const prices = data.map((d) => d.close);
  const sorted = [...prices].sort((a, b) => a - b);
  const mean = prices.reduce((s, p) => s + p, 0) / prices.length;
  const current = prices[prices.length - 1];
  const prev = prices[prices.length - 2];
  return {
    mean: +mean.toFixed(6),
    median: +sorted[Math.floor(sorted.length / 2)].toFixed(6),
    std: +Math.sqrt(prices.reduce((s, p) => s + (p - mean) ** 2, 0) / prices.length).toFixed(6),
    min: +sorted[0].toFixed(6),
    max: +sorted[sorted.length - 1].toFixed(6),
    current: +current.toFixed(6),
    change_pct: +(((current - prev) / prev) * 100).toFixed(2),
  };
}

export function getVolatilityMetrics(data: OHLCData[]): VolatilityMetrics {
  const returns = data.slice(1).map((d, i) => (d.close - data[i].close) / data[i].close);
  const meanReturn = returns.reduce((s, r) => s + r, 0) / returns.length;
  const dailyVol = Math.sqrt(returns.reduce((s, r) => s + (r - meanReturn) ** 2, 0) / returns.length);
  return {
    daily_volatility: +(dailyVol * 100).toFixed(4),
    annual_volatility: +(dailyVol * Math.sqrt(365) * 100).toFixed(2),
    sharpe_ratio: +((meanReturn / dailyVol) * Math.sqrt(365)).toFixed(4),
  };
}

export function getTechnicalData(data: OHLCData[]): TechnicalData {
  const recent = data.slice(-30);
  const firstPrice = recent[0].close;
  const lastPrice = recent[recent.length - 1].close;
  const change = (lastPrice - firstPrice) / firstPrice;
  const trend = change > 0.03 ? "Uptrend" : change < -0.03 ? "Downtrend" : "Sideways";

  // 30-day rolling volatility
  const volatility: { date: string; value: number }[] = [];
  for (let i = 29; i < data.length; i++) {
    const slice = data.slice(i - 29, i + 1);
    const returns = slice.slice(1).map((d, j) => (d.close - slice[j].close) / slice[j].close);
    const mean = returns.reduce((s, r) => s + r, 0) / returns.length;
    const vol = Math.sqrt(returns.reduce((s, r) => s + (r - mean) ** 2, 0) / returns.length);
    volatility.push({ date: data[i].date, value: +(vol * 100).toFixed(4) });
  }

  // Returns distribution
  const allReturns = data.slice(1).map((d, i) => ((d.close - data[i].close) / data[i].close) * 100);
  const bins = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5];
  const distribution = bins.map((b, idx) => {
    const lo = idx === 0 ? -Infinity : b;
    const hi = idx === bins.length - 1 ? Infinity : bins[idx + 1];
    return { bin: `${b}%`, count: allReturns.filter((r) => r >= lo && r < hi).length };
  });

  // Returns stats
  const meanR = allReturns.reduce((s, r) => s + r, 0) / allReturns.length;
  const stdR = Math.sqrt(allReturns.reduce((s, r) => s + (r - meanR) ** 2, 0) / allReturns.length);
  const skew = allReturns.reduce((s, r) => s + ((r - meanR) / stdR) ** 3, 0) / allReturns.length;
  const kurt = allReturns.reduce((s, r) => s + ((r - meanR) / stdR) ** 4, 0) / allReturns.length - 3;

  // RSI
  const rsi: { date: string; value: number }[] = [];
  const rsiData = data.slice(-90);
  for (let i = 14; i < rsiData.length; i++) {
    const slice = rsiData.slice(i - 14, i);
    let gains = 0, losses = 0;
    for (let j = 1; j < slice.length; j++) {
      const diff = slice[j].close - slice[j - 1].close;
      if (diff > 0) gains += diff; else losses -= diff;
    }
    const rs = losses === 0 ? 100 : gains / losses;
    rsi.push({ date: rsiData[i].date, value: +(100 - 100 / (1 + rs)).toFixed(2) });
  }

  return {
    trend,
    volatility,
    returns_distribution: distribution,
    returns_stats: {
      mean_return: +meanR.toFixed(4),
      median_return: +[...allReturns].sort((a, b) => a - b)[Math.floor(allReturns.length / 2)].toFixed(4),
      skewness: +skew.toFixed(4),
      kurtosis: +kurt.toFixed(4),
      positive_days: +(allReturns.filter((r) => r > 0).length / allReturns.length * 100).toFixed(1),
    },
    rsi,
  };
}

export function generateForecast(ticker: string, days: number, models: string[]): Promise<ForecastResult[]> {
  return new Promise((resolve) => {
    setTimeout(() => {
      const data = generateOHLCData(ticker);
      const lastPrice = data[data.length - 1].close;
      const results: ForecastResult[] = models.map((model) => {
        const rand = seededRandom(model.charCodeAt(0) * 71 + ticker.charCodeAt(0));
        const predictions: { date: string; price: number }[] = [];
        let price = lastPrice;
        for (let i = 1; i <= days; i++) {
          const date = new Date();
          date.setDate(date.getDate() + i);
          const drift = model === "LSTM" ? 0.001 : model === "Prophet" ? 0.0005 : 0;
          price = price * (1 + drift + (rand() - 0.49) * 0.02);
          predictions.push({ date: date.toISOString().split("T")[0], price: +price.toFixed(6) });
        }
        return { model, predictions };
      });
      resolve(results);
    }, 1500 + Math.random() * 1500);
  });
}

export function getCorrelationMatrix(tickers: string[]): CorrelationMatrix {
  const allData = tickers.map((t) => generateOHLCData(t, 90).map((d) => d.close));
  const matrix: number[][] = [];
  for (let i = 0; i < tickers.length; i++) {
    const row: number[] = [];
    for (let j = 0; j < tickers.length; j++) {
      if (i === j) { row.push(1); continue; }
      const a = allData[i], b = allData[j];
      const n = Math.min(a.length, b.length);
      const ma = a.slice(0, n).reduce((s, v) => s + v, 0) / n;
      const mb = b.slice(0, n).reduce((s, v) => s + v, 0) / n;
      let num = 0, da = 0, db = 0;
      for (let k = 0; k < n; k++) {
        num += (a[k] - ma) * (b[k] - mb);
        da += (a[k] - ma) ** 2;
        db += (b[k] - mb) ** 2;
      }
      row.push(+(num / Math.sqrt(da * db)).toFixed(4));
    }
    matrix.push(row);
  }
  return { tickers, matrix };
}
