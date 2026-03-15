import { IsString, IsOptional } from 'class-validator';

export class BattleRequestDto {
  @IsString()
  @IsOptional()
  pokemonA?: string;

  @IsString()
  @IsOptional()
  pokemonB?: string;
}
