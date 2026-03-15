package com.srearena

import io.ktor.client.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.server.testing.*
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.Assertions.*

class IntegrationTest {
    @Test
    fun `liveness probe should return alive`() = testApplication {
        application {
            module()
        }
        val response = client.get("/health/live")
        assertEquals(HttpStatusCode.OK, response.status)
        assertTrue(response.bodyAsText().contains("alive"))
    }

    @Test
    fun `readiness probe should return status`() = testApplication {
        application {
            module()
        }
        val response = client.get("/health/ready")
        assertTrue(response.status == HttpStatusCode.OK || response.status == HttpStatusCode.ServiceUnavailable)
    }
}
