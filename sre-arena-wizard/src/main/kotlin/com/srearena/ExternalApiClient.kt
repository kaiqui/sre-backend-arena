package com.srearena

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.serialization.kotlinx.json.*
import kotlinx.serialization.json.Json
import org.slf4j.LoggerFactory
import java.net.URLEncoder

class ExternalApiClient(
    private val baseUrl: String,
    private val timeoutMs: Long
) {
    private val logger = LoggerFactory.getLogger(ExternalApiClient::class.java)

    private val client = HttpClient(CIO) {
        install(HttpTimeout) {
            requestTimeoutMillis = timeoutMs
            connectTimeoutMillis = timeoutMs / 2
        }
        install(ContentNegotiation) {
            json(Json { ignoreUnknownKeys = true })
        }
    }

    suspend fun fetchWizard(name: String): WizardApiData {
        val encodedName = URLEncoder.encode(name, "UTF-8")
        val url = "$baseUrl/characters?filter[name]=$encodedName"
        logger.debug("Fetching wizard data from: $url")

        val response: HttpResponse = client.get(url)
        val body = response.bodyAsText()

        // Parse response - PotterDB returns data array
        val json = Json { ignoreUnknownKeys = true }
        val parsed = json.parseToJsonElement(body)

        val dataArray = parsed.jsonObject["data"]?.jsonArray
        val first = dataArray?.firstOrNull()?.jsonObject

        return WizardApiData(
            name = first?.get("attributes")?.jsonObject?.get("name")?.toString()?.trim('"') ?: name,
            house = first?.get("attributes")?.jsonObject?.get("house")?.toString()?.trim('"'),
            species = first?.get("attributes")?.jsonObject?.get("species")?.toString()?.trim('"'),
            wizard = first?.get("attributes")?.jsonObject?.get("wizard")?.toString()?.toBoolean()
        )
    }
}
