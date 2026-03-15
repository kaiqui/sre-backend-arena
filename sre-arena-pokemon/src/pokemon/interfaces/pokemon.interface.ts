export interface PokemonStat {
  base_stat: number;
  stat: { name: string };
}

export interface PokemonData {
  id: number;
  name: string;
  stats: PokemonStat[];
  types: Array<{ type: { name: string } }>;
}
