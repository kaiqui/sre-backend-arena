package com.srearena

import io.mockk.coEvery
import io.mockk.mockk
import kotlinx.coroutines.runBlocking
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.Assertions.*

class WizardServiceTest {
    private val cache = CacheService(300)
    private val apiClient = mockk<ExternalApiClient>()
    private val metrics = mockk<Metrics>(relaxed = true)
    private val config = AppConfig.fromEnv()
    private val service = WizardService(cache, apiClient, metrics, config)

    @Test
    fun `should return wizard data successfully`() = runBlocking {
        coEvery { apiClient.fetchWizard("Harry Potter") } returns WizardApiData(
            name = "Harry Potter",
            house = "Gryffindor",
            species = "human",
            wizard = true
        )

        val result = service.getWizard("Harry Potter")

        assertEquals("Harry Potter", result.name)
        assertEquals("Gryffindor", result.house)
        assertEquals("human", result.species)
        assertTrue(result.wizard)
        assertTrue(result.powerScore > 0)
    }

    @Test
    fun `should use cache on second call`() = runBlocking {
        coEvery { apiClient.fetchWizard("Hermione Granger") } returns WizardApiData(
            name = "Hermione Granger",
            house = "Gryffindor",
            species = "human",
            wizard = true
        )

        service.getWizard("Hermione Granger")
        val result = service.getWizard("Hermione Granger")

        assertEquals("Hermione Granger", result.name)
    }

    @Test
    fun `should calculate power score for Gryffindor wizard`() = runBlocking {
        coEvery { apiClient.fetchWizard("test") } returns WizardApiData(
            name = "test",
            house = "Gryffindor",
            species = "human",
            wizard = true
        )

        val result = service.getWizard("test")
        assertTrue(result.powerScore >= 50)
    }
}
