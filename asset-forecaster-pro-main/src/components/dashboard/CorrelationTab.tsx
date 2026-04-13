import { useState, useMemo } from "react";
import { AlertTriangle } from "lucide-react";
import { getCryptos, getCorrelationMatrix } from "@/lib/mock-data";

export function CorrelationTab() {
  const cryptos = getCryptos();
  const [selected, setSelected] = useState<string[]>(cryptos.slice(0, 10).map((c) => c.symbol));

  const toggle = (sym: string) => {
    setSelected((prev) => {
      if (prev.includes(sym)) return prev.filter((s) => s !== sym);
      if (prev.length >= 20) return prev;
      return [...prev, sym];
    });
  };

  const matrix = useMemo(() => {
    if (selected.length < 2) return null;
    return getCorrelationMatrix(selected);
  }, [selected]);

  const getColor = (val: number) => {
    if (val >= 0.7) return "bg-primary/80 text-primary-foreground";
    if (val >= 0.3) return "bg-primary/40";
    if (val >= -0.3) return "bg-muted";
    if (val >= -0.7) return "bg-loss/40";
    return "bg-loss/80 text-primary-foreground";
  };

  return (
    <div className="space-y-6">
      {/* Multi-select */}
      <div className="glass-card p-5 animate-fade-in">
        <h3 className="text-lg font-semibold mb-3">Select Cryptocurrencies (max 20)</h3>
        <div className="flex flex-wrap gap-2">
          {cryptos.map((c) => (
            <button
              key={c.symbol}
              onClick={() => toggle(c.symbol)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                selected.includes(c.symbol)
                  ? "bg-primary text-primary-foreground"
                  : "bg-secondary text-secondary-foreground hover:bg-secondary/80"
              }`}
            >
              {c.symbol}
            </button>
          ))}
        </div>
      </div>

      {selected.length < 2 && (
        <div className="glass-card p-5 flex items-center gap-3 text-warning animate-fade-in">
          <AlertTriangle className="w-5 h-5" />
          <span className="text-sm font-medium">Select at least 2 cryptocurrencies for correlation analysis</span>
        </div>
      )}

      {matrix && (
        <>
          {/* Heatmap */}
          <div className="glass-card p-5 animate-fade-in overflow-x-auto">
            <h3 className="text-lg font-semibold mb-4">Correlation Heatmap</h3>
            <div className="inline-block min-w-full">
              <table className="text-xs">
                <thead>
                  <tr>
                    <th className="p-1.5" />
                    {matrix.tickers.map((t) => (
                      <th key={t} className="p-1.5 font-mono font-medium text-muted-foreground">{t}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {matrix.tickers.map((t, i) => (
                    <tr key={t}>
                      <td className="p-1.5 font-mono font-medium text-muted-foreground">{t}</td>
                      {matrix.matrix[i].map((val, j) => (
                        <td
                          key={j}
                          className={`p-1.5 text-center font-mono rounded ${getColor(val)}`}
                          title={`${t} × ${matrix.tickers[j]}: ${val}`}
                        >
                          {val.toFixed(2)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="flex items-center gap-2 mt-4 text-xs text-muted-foreground">
              <span className="inline-block w-4 h-3 bg-loss/80 rounded" /> Strong Negative
              <span className="inline-block w-4 h-3 bg-muted rounded ml-2" /> Neutral
              <span className="inline-block w-4 h-3 bg-primary/80 rounded ml-2" /> Strong Positive
            </div>
          </div>
        </>
      )}
    </div>
  );
}
