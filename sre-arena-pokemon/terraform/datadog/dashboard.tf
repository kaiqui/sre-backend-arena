resource "datadog_dashboard" "pokemon_battle" {
  title       = "Pokemon Battle API - SRE Dashboard"
  layout_type = "ordered"

  widget {
    timeseries_definition {
      title = "Battle Request Rate"
      request {
        q = "sum:pokemon_battle.battle.count{env:prod}.as_rate()"
      }
    }
  }

  widget {
    timeseries_definition {
      title = "Battle Duration p99 (ms)"
      request {
        q = "p99:pokemon_battle.battle.duration{env:prod}"
      }
    }
  }

  widget {
    timeseries_definition {
      title = "Cache Hit Rate (%)"
      request {
        q = "sum:pokemon_battle.cache.hits{env:prod}.as_rate() / (sum:pokemon_battle.cache.hits{env:prod}.as_rate() + sum:pokemon_battle.cache.misses{env:prod}.as_rate()) * 100"
      }
    }
  }

  widget {
    timeseries_definition {
      title = "External API Calls"
      request {
        q = "sum:pokemon_battle.external_api.success{env:prod}.as_rate()"
      }
    }
  }

  tags = ["env:prod", "service:pokemon-battle-api", "team:sre"]
}
