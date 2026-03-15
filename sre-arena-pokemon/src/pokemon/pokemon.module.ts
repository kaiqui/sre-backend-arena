import { Module } from '@nestjs/common';
import { PokemonService } from './pokemon.service';
import { CacheModule } from '../cache/cache.module';
import { ExternalApiModule } from '../external-api/external-api.module';

@Module({
  imports: [CacheModule, ExternalApiModule],
  providers: [PokemonService],
  exports: [PokemonService],
})
export class PokemonModule {}
