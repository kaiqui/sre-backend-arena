resource "datadog_monitor" "high_error_rate" {
  name    = "Wizard API - High Error Rate"
  type    = "metric alert"
  message = "Error rate > 1% for Wizard API. Notify: @pagerduty-sre"

  query = "sum(last_5m):sum:wizard.request.errors{env:prod}.as_rate() / sum:wizard.requests{env:prod}.as_rate() * 100 > 1"

  thresholds = {
    critical = 1
    warning  = 0.5
  }

  tags = ["env:prod", "service:wizard-api"]
}

resource "datadog_monitor" "high_latency" {
  name    = "Wizard API - High Latency p99"
  type    = "metric alert"
  message = "p99 latency > 300ms for Wizard API. Notify: @pagerduty-sre"

  query = "avg(last_5m):p99:wizard.request.duration{env:prod} > 300"

  thresholds = {
    critical = 300
    warning  = 200
  }

  tags = ["env:prod", "service:wizard-api"]
}

resource "datadog_monitor" "rate_limit_violations" {
  name    = "Wizard API - External API Rate Limit Violations"
  type    = "metric alert"
  message = "Rate limit violations detected for Harry Potter API. Notify: @pagerduty-sre"

  query = "sum(last_5m):sum:wizard.external_api.rate_limit_violations{env:prod} > 0"

  thresholds = {
    critical = 0
  }

  tags = ["env:prod", "service:wizard-api"]
}
