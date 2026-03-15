import { Injectable, Logger } from '@nestjs/common';
import { CacheService } from '../cache/cache.service';
import { ExternalApiService } from '../external-api/external-api.service';
import { PokemonData } from './interfaces/pokemon.interface';

@Injectable()
export class PokemonService {
  private readonly logger = new Logger(PokemonService.name);

  constructor(
    private readonly cacheService: CacheService,
    private readonly externalApiService: ExternalApiService,
  ) {}

  async getPokemon(name: string): Promise<PokemonData> {
    const cacheKey = `pokemon:${name}`;
    const cached = this.cacheService.get<PokemonData>(cacheKey);
    if (cached) {
      this.logger.debug(`Cache hit for pokemon: ${name}`);
      return cached;
    }

    const data = await this.externalApiService.fetchPokemon(name);
    this.cacheService.set(cacheKey, data);
    return data;
  }
}
