import { Injectable, Logger } from '@nestjs/common';
import { PokemonService } from '../pokemon/pokemon.service';
import { MetricsService } from '../metrics/metrics.service';
import { BattleResult } from './interfaces/battle-result.interface';

@Injectable()
export class BattleService {
  private readonly logger = new Logger(BattleService.name);

  constructor(
    private readonly pokemonService: PokemonService,
    private readonly metricsService: MetricsService,
  ) {}

  async battle(pokemonA: string, pokemonB: string): Promise<BattleResult> {
    const start = Date.now();
    const [dataA, dataB] = await Promise.all([
      this.pokemonService.getPokemon(pokemonA),
      this.pokemonService.getPokemon(pokemonB),
    ]);

    const totalA = this.calculateTotalStats(dataA.stats);
    const totalB = this.calculateTotalStats(dataB.stats);

    const winner = totalA >= totalB ? pokemonA : pokemonB;
    const reason = 'higher_total_stats';

    const result: BattleResult = {
      pokemonA,
      pokemonB,
      winner,
      reason,
    };

    const duration = Date.now() - start;
    this.metricsService.recordBattleDuration(duration);
    this.logger.log({ message: 'Battle completed', pokemonA, pokemonB, winner, duration });

    return result;
  }

  private calculateTotalStats(stats: Array<{ base_stat: number }>): number {
    return stats.reduce((sum, s) => sum + s.base_stat, 0);
  }
}
