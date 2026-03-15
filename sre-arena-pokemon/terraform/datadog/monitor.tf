resource "datadog_monitor" "high_error_rate" {
  name    = "Pokemon Battle API - High Error Rate"
  type    = "metric alert"
  message = "Error rate > 1% for Pokemon Battle API. Notify: @pagerduty-sre"

  query = "sum(last_5m):sum:pokemon_battle.external_api.error{env:prod}.as_rate() / (sum:pokemon_battle.external_api.success{env:prod}.as_rate() + sum:pokemon_battle.external_api.error{env:prod}.as_rate()) * 100 > 1"

  thresholds = {
    critical = 1
    warning  = 0.5
  }

  tags = ["env:prod", "service:pokemon-battle-api"]
}

resource "datadog_monitor" "high_latency" {
  name    = "Pokemon Battle API - High Latency p99"
  type    = "metric alert"
  message = "p99 battle latency > 300ms. Notify: @pagerduty-sre"

  query = "avg(last_5m):p99:pokemon_battle.battle.duration{env:prod} > 300"

  thresholds = {
    critical = 300
    warning  = 200
  }

  tags = ["env:prod", "service:pokemon-battle-api"]
}

resource "datadog_monitor" "slo_burn_rate" {
  name    = "Pokemon Battle API - SLO Burn Rate"
  type    = "slo alert"
  message = "SLO burn rate is too high. Notify: @pagerduty-sre"

  query = "burn_rate(\"${datadog_service_level_objective.battle_latency.id}\").over(\"1h\") > 14.4"

  thresholds = {
    critical = 14.4
  }

  tags = ["env:prod", "service:pokemon-battle-api"]
}
