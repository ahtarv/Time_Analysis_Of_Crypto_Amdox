import { useState } from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
} from "recharts";
import { Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Checkbox } from "@/components/ui/checkbox";
import { toast } from "sonner";
import { generateForecast, generateOHLCData } from "@/lib/mock-data";
import type { ForecastResult, OHLCData } from "@/types/crypto";

interface ForecastTabProps {
  ticker: string;
}

const MODEL_COLORS: Record<string, string> = {
  ARIMA: "hsl(var(--chart-1))",
  Prophet: "hsl(var(--chart-2))",
  LSTM: "hsl(var(--chart-3))",
};

export function ForecastTab({ ticker }: ForecastTabProps) {
  const [days, setDays] = useState(30);
  const [selectedModels, setSelectedModels] = useState<string[]>(["ARIMA", "Prophet"]);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<ForecastResult[] | null>(null);

  const toggleModel = (model: string) => {
    setSelectedModels((prev) =>
      prev.includes(model) ? prev.filter((m) => m !== model) : [...prev, model]
    );
  };

  const runForecast = async () => {
    if (selectedModels.length === 0) {
      toast.error("Select at least one model");
      return;
    }
    setLoading(true);
    try {
      const res = await generateForecast(ticker, days, selectedModels);
      setResults(res);
      res.forEach((r) => toast.success(`${r.model} forecast generated`));
    } catch {
      toast.error("Forecast failed");
    } finally {
      setLoading(false);
    }
  };

  // Build combined chart data
  const historicalData = generateOHLCData(ticker).slice(-60);
  const chartData: Record<string, any>[] = historicalData.map((d) => ({
    date: d.date,
    historical: d.close,
  }));

  if (results) {
    const maxLen = Math.max(...results.map((r) => r.predictions.length));
    for (let i = 0; i < maxLen; i++) {
      const entry: Record<string, any> = { date: results[0]?.predictions[i]?.date || "" };
      results.forEach((r) => {
        if (r.predictions[i]) entry[r.model] = r.predictions[i].price;
      });
      chartData.push(entry);
    }
  }

  return (
    <div className="space-y-6">
      <div className="glass-card p-6 animate-fade-in">
        <h3 className="text-lg font-semibold mb-5">Forecast Configuration</h3>

        <div className="space-y-5">
          <div>
            <label className="text-sm font-medium text-muted-foreground mb-2 block">
              Forecast Days: <span className="text-foreground font-mono">{days}</span>
            </label>
            <Slider
              value={[days]}
              onValueChange={(v) => setDays(v[0])}
              min={7}
              max={90}
              step={1}
              className="w-full max-w-md"
            />
          </div>

          <div>
            <label className="text-sm font-medium text-muted-foreground mb-3 block">Models</label>
            <div className="flex gap-5">
              {["ARIMA", "Prophet", "LSTM"].map((model) => (
                <label key={model} className="flex items-center gap-2 cursor-pointer">
                  <Checkbox
                    checked={selectedModels.includes(model)}
                    onCheckedChange={() => toggleModel(model)}
                  />
                  <span className="text-sm font-medium">{model}</span>
                </label>
              ))}
            </div>
          </div>

          <Button onClick={runForecast} disabled={loading} className="mt-2">
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Training Models...
              </>
            ) : (
              "Generate Forecast"
            )}
          </Button>
        </div>
      </div>

      {/* Forecast Chart */}
      <div className="glass-card p-5 animate-fade-in">
        <h3 className="text-lg font-semibold mb-4">
          {results ? "Forecast Comparison" : "Historical Price (Last 60 Days)"}
        </h3>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
            <XAxis dataKey="date" tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }} tickFormatter={(v) => v?.slice(5) || ""} interval={Math.floor(chartData.length / 8)} />
            <YAxis tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }} domain={["auto", "auto"]} />
            <Tooltip contentStyle={{ backgroundColor: "hsl(var(--card))", border: "1px solid hsl(var(--border))", borderRadius: "8px", fontSize: 12 }} />
            <Legend />
            <Line type="monotone" dataKey="historical" stroke="hsl(var(--foreground))" strokeWidth={2} dot={false} name="Historical" />
            {results?.map((r) => (
              <Line
                key={r.model}
                type="monotone"
                dataKey={r.model}
                stroke={MODEL_COLORS[r.model]}
                strokeWidth={2}
                strokeDasharray="6 3"
                dot={false}
                name={`${r.model} Forecast`}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Forecast Table */}
      {results && (
        <div className="glass-card p-5 animate-fade-in overflow-x-auto">
          <h3 className="text-lg font-semibold mb-4">Forecast Values</h3>
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border">
                <th className="py-2 text-left text-muted-foreground font-medium">Date</th>
                {results.map((r) => (
                  <th key={r.model} className="py-2 text-right text-muted-foreground font-medium">
                    {r.model}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {results[0].predictions.slice(0, 15).map((p, i) => (
                <tr key={p.date} className="border-b border-border/50">
                  <td className="py-2 font-mono text-muted-foreground">{p.date}</td>
                  {results.map((r) => (
                    <td key={r.model} className="py-2 text-right font-mono">
                      ${r.predictions[i]?.price.toLocaleString(undefined, { maximumFractionDigits: 2 })}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
          {results[0].predictions.length > 15 && (
            <p className="text-xs text-muted-foreground mt-2">Showing first 15 of {results[0].predictions.length} predictions</p>
          )}
        </div>
      )}
    </div>
  );
}
