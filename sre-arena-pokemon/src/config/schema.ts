import * as Joi from 'joi';

export default Joi.object({
  PORT: Joi.number().default(3000),
  POKEAPI_BASE_URL: Joi.string().default('https://pokeapi.co/api/v2'),
  POKEAPI_TIMEOUT_MS: Joi.number().default(3000),
  CACHE_TTL_MS: Joi.number().default(86400000), // 24h
  RATE_LIMIT_PER_MIN: Joi.number().default(90),
  DD_SERVICE: Joi.string().default('pokemon-battle-api'),
  DD_ENV: Joi.string().default('production'),
  DD_VERSION: Joi.string().default('1.0.0'),
  DD_AGENT_HOST: Joi.string().default('localhost'),
  DD_DOGSTATSD_PORT: Joi.number().default(8125),
});
