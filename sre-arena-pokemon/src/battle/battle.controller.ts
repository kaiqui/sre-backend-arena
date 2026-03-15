import { Controller, Get, Query, BadRequestException } from '@nestjs/common';
import { BattleService } from './battle.service';
import { BattleRequestDto } from './dto/battle-request.dto';
import { BattleResult } from './interfaces/battle-result.interface';

@Controller()
export class BattleController {
  constructor(private readonly battleService: BattleService) {}

  @Get('battle')
  async battle(@Query() query: BattleRequestDto): Promise<BattleResult> {
    if (!query.pokemonA || !query.pokemonB) {
      throw new BadRequestException('pokemonA and pokemonB are required');
    }
    return this.battleService.battle(query.pokemonA.toLowerCase(), query.pokemonB.toLowerCase());
  }
}
