package com.srearena

import io.github.resilience4j.circuitbreaker.CircuitBreaker
import io.github.resilience4j.circuitbreaker.CircuitBreakerConfig
import io.github.resilience4j.retry.Retry
import io.github.resilience4j.retry.RetryConfig
import io.github.resilience4j.ratelimiter.RateLimiter
import io.github.resilience4j.ratelimiter.RateLimiterConfig
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.slf4j.LoggerFactory
import java.time.Duration

data class WizardResponse(
    val name: String,
    val house: String,
    val species: String,
    val wizard: Boolean,
    val powerScore: Int
)

class WizardService(
    private val cache: CacheService,
    private val apiClient: ExternalApiClient,
    private val metrics: Metrics,
    private val config: AppConfig
) {
    private val logger = LoggerFactory.getLogger(WizardService::class.java)

    private val circuitBreaker = CircuitBreaker.of("wizard-api",
        CircuitBreakerConfig.custom()
            .failureRateThreshold(50f)
            .waitDurationInOpenState(Duration.ofSeconds(30))
            .slidingWindowSize(10)
            .build()
    )

    private val retry = Retry.of("wizard-api",
        RetryConfig.custom<Any>()
            .maxAttempts(3)
            .waitDuration(Duration.ofMillis(100))
            .exponentialBackoffMultiplier(2.0)
            .build()
    )

    private val rateLimiter = RateLimiter.of("potter-api",
        RateLimiterConfig.custom()
            .limitForPeriod(config.rateLimitPerMin)
            .limitRefreshPeriod(Duration.ofMinutes(1))
            .timeoutDuration(Duration.ofMillis(500))
            .build()
    )

    suspend fun getWizard(name: String): WizardResponse {
        val cacheKey = "wizard:${name.lowercase()}"
        cache.get<WizardResponse>(cacheKey)?.let {
            logger.debug("Cache hit for wizard: $name")
            metrics.incrementCacheHits()
            return it
        }
        metrics.incrementCacheMisses()

        val wizardData = withContext(Dispatchers.IO) {
            rateLimiter.executeCallable {
                circuitBreaker.executeCallable {
                    retry.executeCallable {
                        apiClient.fetchWizard(name)
                    }
                }
            }
        }

        val response = WizardResponse(
            name = wizardData.name,
            house = wizardData.house ?: "Unknown",
            species = wizardData.species ?: "human",
            wizard = wizardData.wizard ?: true,
            powerScore = calculatePowerScore(wizardData)
        )

        cache.put(cacheKey, response)
        return response
    }

    private fun calculatePowerScore(data: WizardApiData): Int {
        var score = 50
        score += when (data.house?.lowercase()) {
            "gryffindor" -> 20
            "slytherin" -> 18
            "ravenclaw" -> 15
            "hufflepuff" -> 12
            else -> 0
        }
        if (data.wizard == true) score += 15
        score += when (data.species?.lowercase()) {
            "human" -> 5
            "half-giant" -> 10
            "werewolf" -> 8
            else -> 0
        }
        return minOf(100, score)
    }

    fun isReady(): Boolean {
        return circuitBreaker.state != CircuitBreaker.State.OPEN
    }
}

data class WizardApiData(
    val name: String,
    val house: String?,
    val species: String?,
    val wizard: Boolean?
)
