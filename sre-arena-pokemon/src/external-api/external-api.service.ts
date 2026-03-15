import { Injectable, Logger, ServiceUnavailableException } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import CircuitBreaker from 'opossum';
import { PokemonData } from '../pokemon/interfaces/pokemon.interface';

@Injectable()
export class ExternalApiService {
  private readonly logger = new Logger(ExternalApiService.name);
  private readonly baseUrl: string;
  private readonly timeoutMs: number;
  private readonly circuitBreaker: CircuitBreaker;
  private requestTimestamps: number[] = [];
  private readonly rateLimitPerMin: number;

  constructor(private readonly config: ConfigService) {
    this.baseUrl = this.config.get<string>('POKEAPI_BASE_URL', 'https://pokeapi.co/api/v2');
    this.timeoutMs = this.config.get<number>('POKEAPI_TIMEOUT_MS', 3000);
    this.rateLimitPerMin = this.config.get<number>('RATE_LIMIT_PER_MIN', 90);

    this.circuitBreaker = new CircuitBreaker(this.fetchFromApi.bind(this), {
      timeout: this.timeoutMs,
      errorThresholdPercentage: 50,
      resetTimeout: 30000,
    });

    this.circuitBreaker.fallback(() => {
      throw new ServiceUnavailableException('External API temporarily unavailable');
    });
  }

  private checkRateLimit(): void {
    const now = Date.now();
    this.requestTimestamps = this.requestTimestamps.filter(ts => now - ts < 60000);
    if (this.requestTimestamps.length >= this.rateLimitPerMin) {
      throw new ServiceUnavailableException('Rate limit reached for external API');
    }
    this.requestTimestamps.push(now);
  }

  private async fetchFromApi(name: string): Promise<PokemonData> {
    const url = `${this.baseUrl}/pokemon/${name}`;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const response = await fetch(url, { signal: controller.signal });
      if (!response.ok) {
        throw new Error(`API returned ${response.status}`);
      }
      return response.json() as Promise<PokemonData>;
    } finally {
      clearTimeout(timeout);
    }
  }

  async fetchPokemon(name: string): Promise<PokemonData> {
    this.checkRateLimit();
    return this.circuitBreaker.fire(name) as Promise<PokemonData>;
  }
}
