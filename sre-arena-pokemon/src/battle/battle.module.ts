import { Module } from '@nestjs/common';
import { BattleController } from './battle.controller';
import { BattleService } from './battle.service';
import { PokemonModule } from '../pokemon/pokemon.module';
import { MetricsModule } from '../metrics/metrics.module';

@Module({
  imports: [PokemonModule, MetricsModule],
  controllers: [BattleController],
  providers: [BattleService],
})
export class BattleModule {}
