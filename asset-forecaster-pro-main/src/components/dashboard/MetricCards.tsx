import { TrendingUp, TrendingDown, DollarSign, BarChart3 } from "lucide-react";
import type { PriceStatistics } from "@/types/crypto";

interface MetricCardsProps {
  stats: PriceStatistics;
  ticker: string;
}

const formatPrice = (price: number) => {
  if (price < 0.01) return `$${price.toFixed(6)}`;
  if (price < 1) return `$${price.toFixed(4)}`;
  return `$${price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
};

export function MetricCards({ stats, ticker }: MetricCardsProps) {
  const cards = [
    {
      label: "Current Price",
      value: formatPrice(stats.current),
      icon: DollarSign,
      accent: "primary" as const,
    },
    {
      label: "Change %",
      value: `${stats.change_pct > 0 ? "+" : ""}${stats.change_pct}%`,
      icon: stats.change_pct >= 0 ? TrendingUp : TrendingDown,
      accent: stats.change_pct >= 0 ? ("gain" as const) : ("loss" as const),
    },
    {
      label: "Max Price",
      value: formatPrice(stats.max),
      icon: TrendingUp,
      accent: "gain" as const,
    },
    {
      label: "Min Price",
      value: formatPrice(stats.min),
      icon: TrendingDown,
      accent: "loss" as const,
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card) => (
        <div
          key={card.label}
          className="glass-card p-5 animate-fade-in group hover:glow-primary transition-all duration-300"
        >
          <div className="flex items-center justify-between mb-3">
            <span className="text-sm font-medium text-muted-foreground">{card.label}</span>
            <card.icon
              className={`w-5 h-5 ${
                card.accent === "gain"
                  ? "text-gain"
                  : card.accent === "loss"
                  ? "text-loss"
                  : "text-primary"
              }`}
            />
          </div>
          <p
            className={`text-2xl font-bold font-mono ${
              card.accent === "gain"
                ? "text-gain"
                : card.accent === "loss"
                ? "text-loss"
                : "text-foreground"
            }`}
          >
            {card.value}
          </p>
          <p className="text-xs text-muted-foreground mt-1">{ticker}</p>
        </div>
      ))}
    </div>
  );
}
