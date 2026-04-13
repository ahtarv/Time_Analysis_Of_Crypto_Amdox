import type { PriceStatistics, VolatilityMetrics } from "@/types/crypto";

interface StatsTablesProps {
  priceStats: PriceStatistics;
  volMetrics: VolatilityMetrics;
}

const formatNum = (n: number) => {
  if (Math.abs(n) < 0.01) return n.toFixed(6);
  if (Math.abs(n) < 1) return n.toFixed(4);
  return n.toLocaleString(undefined, { maximumFractionDigits: 2 });
};

function StatsTable({ title, rows }: { title: string; rows: [string, string][] }) {
  return (
    <div className="glass-card p-5 animate-fade-in">
      <h3 className="text-lg font-semibold mb-4">{title}</h3>
      <table className="w-full text-sm">
        <tbody>
          {rows.map(([label, value]) => (
            <tr key={label} className="border-b border-border/50 last:border-0">
              <td className="py-2.5 text-muted-foreground font-medium">{label}</td>
              <td className="py-2.5 text-right font-mono font-medium">{value}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function StatsTables({ priceStats, volMetrics }: StatsTablesProps) {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <StatsTable
        title="Price Statistics"
        rows={[
          ["Mean", `$${formatNum(priceStats.mean)}`],
          ["Median", `$${formatNum(priceStats.median)}`],
          ["Std Deviation", `$${formatNum(priceStats.std)}`],
          ["Min", `$${formatNum(priceStats.min)}`],
          ["Max", `$${formatNum(priceStats.max)}`],
          ["Current", `$${formatNum(priceStats.current)}`],
          ["Change %", `${priceStats.change_pct > 0 ? "+" : ""}${priceStats.change_pct}%`],
        ]}
      />
      <StatsTable
        title="Volatility Metrics"
        rows={[
          ["Daily Volatility", `${volMetrics.daily_volatility}%`],
          ["Annual Volatility", `${volMetrics.annual_volatility}%`],
          ["Sharpe Ratio", formatNum(volMetrics.sharpe_ratio)],
        ]}
      />
    </div>
  );
}
