package com.srearena

data class AppConfig(
    val port: Int = 8080,
    val externalApiUrl: String = "https://api.potterdb.com/v1",
    val cacheTtlSeconds: Long = 300,
    val externalApiTimeoutMs: Long = 2000,
    val rateLimitPerMin: Int = 90,
    val datadogApiKey: String = "",
    val datadogAppKey: String = "",
    val ddEnv: String = "production",
    val ddService: String = "wizard-api",
    val ddVersion: String = "1.0.0",
    val ddAgentHost: String = "localhost",
    val ddStatsdPort: Int = 8125
) {
    companion object {
        fun fromEnv() = AppConfig(
            port = System.getenv("PORT")?.toInt() ?: 8080,
            externalApiUrl = System.getenv("EXTERNAL_API_URL") ?: "https://api.potterdb.com/v1",
            cacheTtlSeconds = System.getenv("CACHE_TTL_SECONDS")?.toLong() ?: 300,
            externalApiTimeoutMs = System.getenv("EXTERNAL_API_TIMEOUT_MS")?.toLong() ?: 2000,
            rateLimitPerMin = System.getenv("RATE_LIMIT_PER_MIN")?.toInt() ?: 90,
            datadogApiKey = System.getenv("DD_API_KEY") ?: "",
            datadogAppKey = System.getenv("DD_APP_KEY") ?: "",
            ddEnv = System.getenv("DD_ENV") ?: "production",
            ddService = System.getenv("DD_SERVICE") ?: "wizard-api",
            ddVersion = System.getenv("DD_VERSION") ?: "1.0.0",
            ddAgentHost = System.getenv("DD_AGENT_HOST") ?: "localhost",
            ddStatsdPort = System.getenv("DD_DOGSTATSD_PORT")?.toInt() ?: 8125
        )
    }
}
