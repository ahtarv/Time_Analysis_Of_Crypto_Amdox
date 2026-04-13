import {
  ComposedChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Brush,
} from "recharts";
import type { OHLCData } from "@/types/crypto";

interface CandlestickChartProps {
  data: OHLCData[];
}

// Recharts doesn't have native candlestick, so we simulate with bars
export function CandlestickChart({ data }: CandlestickChartProps) {
  const last90 = data.slice(-90).map((d) => ({
    ...d,
    body: [Math.min(d.open, d.close), Math.max(d.open, d.close)],
    wick: [d.low, d.high],
    fill: d.close >= d.open ? "hsl(var(--gain))" : "hsl(var(--loss))",
    change: ((d.close - d.open) / d.open * 100).toFixed(2),
  }));

  return (
    <div className="glass-card p-5 animate-fade-in">
      <h3 className="text-lg font-semibold mb-4">Candlestick Chart (90 Days)</h3>
      <ResponsiveContainer width="100%" height={400}>
        <ComposedChart data={last90}>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 10, fill: "hsl(var(--muted-foreground))" }}
            tickFormatter={(v) => v.slice(5)}
            interval={Math.floor(last90.length / 8)}
          />
          <YAxis
            domain={["auto", "auto"]}
            tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }}
            tickFormatter={(v) => (v < 1 ? v.toFixed(4) : v.toLocaleString())}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "hsl(var(--card))",
              border: "1px solid hsl(var(--border))",
              borderRadius: "8px",
              fontSize: 12,
            }}
            formatter={(_val: unknown, name: string, props: { payload: OHLCData }) => {
              const d = props.payload;
              if (name === "close") return [
                `O: ${d.open} H: ${d.high} L: ${d.low} C: ${d.close}`,
                "OHLC",
              ];
              return null;
            }}
          />
          <Bar
            dataKey="close"
            fill="hsl(var(--chart-1))"
            radius={[2, 2, 0, 0]}
            barSize={4}
            shape={(props: any) => {
              const { x, y, width, payload } = props;
              const isGreen = payload.close >= payload.open;
              const color = isGreen ? "hsl(var(--gain))" : "hsl(var(--loss))";
              const yScale = props.background?.height || 300;
              // Simple bar representation
              return (
                <g>
                  <rect
                    x={x}
                    y={y}
                    width={Math.max(width, 3)}
                    height={Math.max(2, 4)}
                    fill={color}
                    rx={1}
                  />
                </g>
              );
            }}
          />
          <Brush dataKey="date" height={30} stroke="hsl(var(--primary))" />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}
