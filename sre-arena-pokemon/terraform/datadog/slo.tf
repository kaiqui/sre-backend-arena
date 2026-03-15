resource "datadog_service_level_objective" "battle_latency" {
  name        = "Pokemon Battle API - Latency SLO"
  description = "99% of battle requests complete in < 300ms"
  type        = "metric"

  query {
    numerator   = "sum:pokemon_battle.battle.duration{env:prod,quantile:0.99,duration:<300}"
    denominator = "sum:pokemon_battle.battle.duration{env:prod}"
  }

  thresholds {
    timeframe = "1h"
    target    = 99
  }

  thresholds {
    timeframe = "30d"
    target    = 99
  }

  tags = ["env:prod", "service:pokemon-battle-api", "team:sre"]
}
