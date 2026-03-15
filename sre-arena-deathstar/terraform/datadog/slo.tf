resource "datadog_service_level_objective" "availability" {
  name        = "SRE Backend Arena - Availability"
  description = "99.99% availability"
  type        = "metric"

  query {
    numerator   = "sum:sre_api.requests{status:200}"
    denominator = "sum:sre_api.requests{}"
  }

  thresholds {
    timeframe = "30d"
    target    = 99.99
  }

  tags = ["environment:prod", "service:sre-backend"]
}

resource "datadog_service_level_objective" "latency" {
  name        = "SRE Backend Arena - Latency p99 < 500ms"
  description = "P99 latency under 500ms"
  type        = "metric"

  query {
    numerator   = "sum:sre_api.latency{p99:<500}"
    denominator = "sum:sre_api.latency{}"
  }

  thresholds {
    timeframe = "30d"
    target    = 95
  }

  tags = ["environment:prod", "service:sre-backend"]
}
