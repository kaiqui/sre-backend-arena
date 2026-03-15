resource "datadog_dashboard" "wizard_api" {
  title       = "Wizard API - SRE Dashboard"
  layout_type = "ordered"

  widget {
    timeseries_definition {
      title = "Request Rate"
      request {
        q = "sum:wizard.requests{env:prod}.as_rate()"
      }
    }
  }

  widget {
    timeseries_definition {
      title = "p99 Latency (ms)"
      request {
        q = "p99:wizard.request.duration{env:prod}"
      }
    }
  }

  widget {
    timeseries_definition {
      title = "Error Rate (%)"
      request {
        q = "sum:wizard.request.errors{env:prod}.as_rate() / sum:wizard.requests{env:prod}.as_rate() * 100"
      }
    }
  }

  widget {
    timeseries_definition {
      title = "Cache Hit Rate (%)"
      request {
        q = "sum:wizard.cache.hits{env:prod}.as_rate() / (sum:wizard.cache.hits{env:prod}.as_rate() + sum:wizard.cache.misses{env:prod}.as_rate()) * 100"
      }
    }
  }

  tags = ["env:prod", "service:wizard-api", "team:sre"]
}
