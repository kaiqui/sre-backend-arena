package com.srearena

import io.ktor.server.plugins.statuspages.*
import org.slf4j.LoggerFactory
import java.util.concurrent.atomic.AtomicLong

class Metrics(private val config: AppConfig) {
    private val logger = LoggerFactory.getLogger(Metrics::class.java)

    private val requestCount = AtomicLong(0)
    private val errorCount = AtomicLong(0)
    private val cacheHits = AtomicLong(0)
    private val cacheMisses = AtomicLong(0)

    fun recordRequest(endpoint: String, status: String, startTime: Long) {
        requestCount.incrementAndGet()
        if (status == "error") errorCount.incrementAndGet()
    }

    fun incrementCacheHits() = cacheHits.incrementAndGet()
    fun incrementCacheMisses() = cacheMisses.incrementAndGet()

    fun getPrometheusMetrics(): String {
        val total = requestCount.get()
        val errors = errorCount.get()
        val hits = cacheHits.get()
        val misses = cacheMisses.get()
        return """
            # HELP wizard_requests_total Total wizard API requests
            # TYPE wizard_requests_total counter
            wizard_requests_total $total
            # HELP wizard_errors_total Total wizard API errors
            # TYPE wizard_errors_total counter
            wizard_errors_total $errors
            # HELP wizard_cache_hits_total Total cache hits
            # TYPE wizard_cache_hits_total counter
            wizard_cache_hits_total $hits
            # HELP wizard_cache_misses_total Total cache misses
            # TYPE wizard_cache_misses_total counter
            wizard_cache_misses_total $misses
        """.trimIndent()
    }
}
