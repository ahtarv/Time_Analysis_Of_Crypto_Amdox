import { useState, useEffect } from "react";
import { TrendingUp, BarChart3, LineChart, GitBranch, Moon, Sun } from "lucide-react";
import { getCryptos, getCryptoData, getStatistics, getTechnicalData } from "@/lib/api";
import { MetricCards } from "@/components/dashboard/MetricCards";
import { PriceChart } from "@/components/dashboard/PriceChart";
import { CandlestickChart } from "@/components/dashboard/CandlestickChart";
import { StatsTables } from "@/components/dashboard/StatsTables";
import { TechnicalTab } from "@/components/dashboard/TechnicalTab";
import { ForecastTab } from "@/components/dashboard/ForecastTab";
import { CorrelationTab } from "@/components/dashboard/CorrelationTab";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import type { TabType, CryptoTicker, OHLCData, PriceStatistics, VolatilityMetrics, TechnicalData } from "@/types/crypto";

const tabs: { id: TabType; label: string; icon: React.ElementType }[] = [
  { id: "overview", label: "Overview", icon: BarChart3 },
  { id: "technical", label: "Technical Analysis", icon: LineChart },
  { id: "forecasting", label: "Forecasting", icon: TrendingUp },
  { id: "correlation", label: "Correlation", icon: GitBranch },
];

export default function Index() {
  const [ticker, setTicker] = useState("BTC");
  const [activeTab, setActiveTab] = useState<TabType>("overview");
  const [darkMode, setDarkMode] = useState(true);
  const [cryptos, setCryptos] = useState<CryptoTicker[]>([]);
  const [ohlcData, setOhlcData] = useState<OHLCData[]>([]);
  const [priceStats, setPriceStats] = useState<PriceStatistics | null>(null);
  const [volMetrics, setVolMetrics] = useState<VolatilityMetrics | null>(null);
  const [technicalData, setTechnicalData] = useState<TechnicalData | null>(null);
  const [loading, setLoading] = useState(false);

  // Load crypto list on mount
  useEffect(() => {
    getCryptos().then(setCryptos).catch(console.error);
  }, []);

  // Load data when ticker changes
  useEffect(() => {
    if (!ticker) return;
    setLoading(true);
    
    Promise.all([
      getCryptoData(ticker),
      getStatistics(ticker),
      getTechnicalData(ticker)
    ])
      .then(([data, stats, technical]) => {
        setOhlcData(data);
        setPriceStats(stats.price_statistics);
        setVolMetrics(stats.volatility_metrics);
        setTechnicalData(technical);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [ticker]);

  // Toggle dark mode on root element
  const toggleDark = () => {
    setDarkMode((prev) => {
      const next = !prev;
      document.documentElement.classList.toggle("dark", next);
      return next;
    });
  };

  // Initialize dark mode
  useEffect(() => {
    document.documentElement.classList.add("dark");
  }, []);

  return (
    <div className="min-h-screen bg-background transition-colors duration-300">
      {/* Header */}
      <header className="border-b border-border/50 bg-card/50 backdrop-blur-xl sticky top-0 z-50">
        <div className="container max-w-7xl mx-auto px-4 py-4">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-primary" />
              </div>
              <div>
                <h1 className="text-lg font-bold tracking-tight">
                  Crypto Analysis
                </h1>
                <p className="text-xs text-muted-foreground">Time Series Analysis & Forecasting</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <Select value={ticker} onValueChange={setTicker}>
                <SelectTrigger className="w-48 bg-secondary border-border">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {cryptos.map((c) => (
                    <SelectItem key={c.symbol} value={c.symbol}>
                      {c.symbol} — {c.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              <button
                onClick={toggleDark}
                className="w-9 h-9 rounded-lg bg-secondary flex items-center justify-center hover:bg-secondary/80 transition-colors"
              >
                {darkMode ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
              </button>
            </div>
          </div>

          {/* Tabs */}
          <nav className="flex gap-1 mt-4 -mb-px overflow-x-auto">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-2.5 text-sm font-medium rounded-t-lg transition-all whitespace-nowrap ${
                  activeTab === tab.id
                    ? "bg-background text-foreground border border-border border-b-background -mb-px"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                <tab.icon className="w-4 h-4" />
                <span className="hidden sm:inline">{tab.label}</span>
              </button>
            ))}
          </nav>
        </div>
      </header>

      {/* Content */}
      <main className="container max-w-7xl mx-auto px-4 py-6 space-y-6">
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="text-muted-foreground">Loading data...</div>
          </div>
        ) : (
          <>
            {activeTab === "overview" && priceStats && volMetrics && (
              <>
                <MetricCards stats={priceStats} ticker={ticker} />
                <PriceChart data={ohlcData} />
                <CandlestickChart data={ohlcData} />
                <StatsTables priceStats={priceStats} volMetrics={volMetrics} />
              </>
            )}

            {activeTab === "technical" && technicalData && <TechnicalTab data={technicalData} />}
            {activeTab === "forecasting" && <ForecastTab ticker={ticker} />}
            {activeTab === "correlation" && <CorrelationTab />}
          </>
        )}
      </main>

      <footer className="border-t border-border/50 py-4 mt-8">
        <p className="text-center text-xs text-muted-foreground">
          Crypto Analysis — Cryptocurrency Time Series Analysis & Forecasting
        </p>
      </footer>
    </div>
  );
}
