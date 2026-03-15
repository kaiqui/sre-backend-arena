package com.srearena

import io.ktor.server.application.*
import io.ktor.server.engine.*
import io.ktor.server.cio.*
import io.ktor.server.routing.*
import io.ktor.server.response.*
import io.ktor.server.plugins.contentnegotiation.*
import io.ktor.serialization.kotlinx.json.*
import io.ktor.http.*
import kotlinx.serialization.json.Json
import org.slf4j.LoggerFactory

private val logger = LoggerFactory.getLogger("Application")

fun main() {
    val port = System.getenv("PORT")?.toInt() ?: 8080
    embeddedServer(CIO, port = port, module = Application::module).start(wait = true)
}

fun Application.module() {
    install(ContentNegotiation) {
        json(Json {
            prettyPrint = false
            isLenient = true
            ignoreUnknownKeys = true
        })
    }

    val config = AppConfig.fromEnv()
    val cacheService = CacheService(config.cacheTtlSeconds)
    val apiClient = ExternalApiClient(config.externalApiUrl, config.externalApiTimeoutMs)
    val metrics = Metrics(config)
    val wizardService = WizardService(cacheService, apiClient, metrics, config)

    routing {
        get("/wizard/{name}") {
            val name = call.parameters["name"] ?: return@get call.respond(HttpStatusCode.BadRequest, mapOf("error" to "name is required"))
            try {
                val wizard = wizardService.getWizard(name)
                metrics.recordRequest("wizard_lookup", "success", System.currentTimeMillis())
                call.respond(wizard)
            } catch (e: Exception) {
                logger.error("Error fetching wizard $name: ${e.message}")
                metrics.recordRequest("wizard_lookup", "error", System.currentTimeMillis())
                call.respond(HttpStatusCode.ServiceUnavailable, mapOf("error" to "Service temporarily unavailable"))
            }
        }

        get("/health/live") {
            call.respond(mapOf("status" to "alive"))
        }

        get("/health/ready") {
            val ready = wizardService.isReady()
            if (ready) {
                call.respond(mapOf("status" to "ready"))
            } else {
                call.respond(HttpStatusCode.ServiceUnavailable, mapOf("status" to "not_ready"))
            }
        }

        get("/metrics") {
            call.respondText(metrics.getPrometheusMetrics(), ContentType.Text.Plain)
        }
    }
}
