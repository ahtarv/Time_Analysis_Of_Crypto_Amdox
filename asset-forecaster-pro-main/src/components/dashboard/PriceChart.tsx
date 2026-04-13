import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, Brush,
} from "recharts";
import type { OHLCData } from "@/types/crypto";

interface PriceChartProps {
  data: OHLCData[];
}

export function PriceChart({ data }: PriceChartProps) {
  return (
    <div className="glass-card p-5 animate-fade-in">
      <h3 className="text-lg font-semibold mb-4">Price Trend & Moving Averages</h3>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }}
            tickFormatter={(v) => v.slice(5)}
            interval={Math.floor(data.length / 8)}
          />
          <YAxis
            tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }}
            domain={["auto", "auto"]}
            tickFormatter={(v) => (v < 1 ? v.toFixed(4) : v.toLocaleString())}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "hsl(var(--card))",
              border: "1px solid hsl(var(--border))",
              borderRadius: "8px",
              fontSize: 12,
            }}
          />
          <Legend />
          <Line type="monotone" dataKey="close" stroke="hsl(var(--chart-1))" strokeWidth={2} dot={false} name="Price" />
          <Line type="monotone" dataKey="ma7" stroke="hsl(var(--chart-ma7))" strokeWidth={1.5} dot={false} strokeDasharray="4 2" name="MA 7" />
          <Line type="monotone" dataKey="ma30" stroke="hsl(var(--chart-ma30))" strokeWidth={1.5} dot={false} strokeDasharray="4 2" name="MA 30" />
          <Line type="monotone" dataKey="ma90" stroke="hsl(var(--chart-ma90))" strokeWidth={1.5} dot={false} strokeDasharray="6 3" name="MA 90" />
          <Brush dataKey="date" height={30} stroke="hsl(var(--primary))" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
