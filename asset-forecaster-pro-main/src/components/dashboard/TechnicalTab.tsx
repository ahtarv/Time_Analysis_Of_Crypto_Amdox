import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  BarChart, Bar, ReferenceLine, Legend,
} from "recharts";
import type { TechnicalData } from "@/types/crypto";
import { Badge } from "@/components/ui/badge";

interface TechnicalTabProps {
  data: TechnicalData;
}

const formatNum = (n: number) => (Math.abs(n) < 1 ? n.toFixed(4) : n.toFixed(2));

export function TechnicalTab({ data }: TechnicalTabProps) {
  const trendColor =
    data.trend === "Uptrend" ? "bg-gain text-primary-foreground" :
    data.trend === "Downtrend" ? "bg-loss text-primary-foreground" :
    "bg-warning text-primary-foreground";

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <h2 className="text-xl font-bold">Trend Analysis</h2>
        <Badge className={`${trendColor} text-sm px-3 py-1`}>{data.trend}</Badge>
      </div>

      {/* Volatility Chart */}
      <div className="glass-card p-5 animate-fade-in">
        <h3 className="text-lg font-semibold mb-4">30-Day Rolling Volatility</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data.volatility}>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
            <XAxis dataKey="date" tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }} tickFormatter={(v) => v.slice(5)} interval={Math.floor(data.volatility.length / 6)} />
            <YAxis tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }} />
            <Tooltip contentStyle={{ backgroundColor: "hsl(var(--card))", border: "1px solid hsl(var(--border))", borderRadius: "8px", fontSize: 12 }} />
            <Line type="monotone" dataKey="value" stroke="hsl(var(--chart-4))" strokeWidth={2} dot={false} name="Volatility %" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Returns Distribution */}
      <div className="glass-card p-5 animate-fade-in">
        <h3 className="text-lg font-semibold mb-4">Returns Distribution</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data.returns_distribution}>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
            <XAxis dataKey="bin" tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }} />
            <YAxis tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }} />
            <Tooltip contentStyle={{ backgroundColor: "hsl(var(--card))", border: "1px solid hsl(var(--border))", borderRadius: "8px", fontSize: 12 }} />
            <Bar dataKey="count" fill="hsl(var(--chart-1))" radius={[4, 4, 0, 0]} name="Frequency" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Returns Stats Table */}
      <div className="glass-card p-5 animate-fade-in">
        <h3 className="text-lg font-semibold mb-4">Returns Statistics</h3>
        <table className="w-full text-sm">
          <tbody>
            {[
              ["Mean Return", `${formatNum(data.returns_stats.mean_return)}%`],
              ["Median Return", `${formatNum(data.returns_stats.median_return)}%`],
              ["Skewness", formatNum(data.returns_stats.skewness)],
              ["Kurtosis", formatNum(data.returns_stats.kurtosis)],
              ["Positive Days", `${data.returns_stats.positive_days}%`],
            ].map(([label, value]) => (
              <tr key={label} className="border-b border-border/50 last:border-0">
                <td className="py-2.5 text-muted-foreground font-medium">{label}</td>
                <td className="py-2.5 text-right font-mono font-medium">{value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* RSI Chart */}
      <div className="glass-card p-5 animate-fade-in">
        <h3 className="text-lg font-semibold mb-4">RSI (14-day, Last 90 Days)</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data.rsi}>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
            <XAxis dataKey="date" tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }} tickFormatter={(v) => v.slice(5)} interval={Math.floor(data.rsi.length / 6)} />
            <YAxis domain={[0, 100]} tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }} />
            <Tooltip contentStyle={{ backgroundColor: "hsl(var(--card))", border: "1px solid hsl(var(--border))", borderRadius: "8px", fontSize: 12 }} />
            <ReferenceLine y={70} stroke="hsl(var(--loss))" strokeDasharray="5 5" label={{ value: "Overbought (70)", fill: "hsl(var(--loss))", fontSize: 11 }} />
            <ReferenceLine y={30} stroke="hsl(var(--gain))" strokeDasharray="5 5" label={{ value: "Oversold (30)", fill: "hsl(var(--gain))", fontSize: 11 }} />
            <Line type="monotone" dataKey="value" stroke="hsl(var(--chart-3))" strokeWidth={2} dot={false} name="RSI" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
