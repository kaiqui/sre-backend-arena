package com.srearena

import com.github.benmanes.caffeine.cache.Caffeine
import org.slf4j.LoggerFactory
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicLong

class CacheService(private val ttlSeconds: Long) {
    private val logger = LoggerFactory.getLogger(CacheService::class.java)
    private val hits = AtomicLong(0)
    private val misses = AtomicLong(0)

    private val cache = Caffeine.newBuilder()
        .maximumSize(10_000)
        .expireAfterWrite(ttlSeconds, TimeUnit.SECONDS)
        .recordStats()
        .build<String, Any>()

    @Suppress("UNCHECKED_CAST")
    fun <T> get(key: String): T? {
        return cache.getIfPresent(key) as? T
    }

    fun <T : Any> put(key: String, value: T) {
        cache.put(key, value)
    }

    fun invalidate(key: String) {
        cache.invalidate(key)
    }

    fun getStats(): Map<String, Long> {
        val stats = cache.stats()
        return mapOf(
            "hits" to stats.hitCount(),
            "misses" to stats.missCount(),
            "size" to cache.estimatedSize()
        )
    }
}
