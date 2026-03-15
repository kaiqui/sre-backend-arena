resource "datadog_service_level_objective" "wizard_latency" {
  name        = "Wizard API - Latency SLO"
  description = "99% of requests complete in < 300ms"
  type        = "metric"

  query {
    numerator   = "sum:wizard.request.duration{env:prod,quantile:0.99,duration:<300}"
    denominator = "sum:wizard.request.duration{env:prod}"
  }

  thresholds {
    timeframe = "1h"
    target    = 99
  }

  thresholds {
    timeframe = "30d"
    target    = 99
  }

  tags = ["env:prod", "service:wizard-api", "team:sre"]
}
