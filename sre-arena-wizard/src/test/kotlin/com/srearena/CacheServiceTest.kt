package com.srearena

import org.junit.jupiter.api.Test
import org.junit.jupiter.api.Assertions.*

class CacheServiceTest {
    private val cache = CacheService(300)

    @Test
    fun `should store and retrieve value`() {
        cache.put("key1", "value1")
        assertEquals("value1", cache.get<String>("key1"))
    }

    @Test
    fun `should return null for missing key`() {
        assertNull(cache.get<String>("missing_key"))
    }

    @Test
    fun `should invalidate key`() {
        cache.put("key2", "value2")
        cache.invalidate("key2")
        assertNull(cache.get<String>("key2"))
    }

    @Test
    fun `should track stats`() {
        cache.put("key3", "value3")
        cache.get<String>("key3")
        val stats = cache.getStats()
        assertNotNull(stats["hits"])
        assertNotNull(stats["misses"])
    }
}
