import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import StatsD from 'hot-shots';

@Injectable()
export class MetricsService {
  private readonly logger = new Logger(MetricsService.name);
  private readonly statsd: StatsD;

  constructor(private readonly config: ConfigService) {
    this.statsd = new StatsD({
      host: this.config.get<string>('DD_AGENT_HOST', 'localhost'),
      port: this.config.get<number>('DD_DOGSTATSD_PORT', 8125),
      prefix: 'pokemon_battle.',
      globalTags: {
        env: this.config.get<string>('DD_ENV', 'production'),
        service: this.config.get<string>('DD_SERVICE', 'pokemon-battle-api'),
        version: this.config.get<string>('DD_VERSION', '1.0.0'),
      },
      errorHandler: (err) => this.logger.warn(`StatsD error: ${err.message}`),
    });
  }

  recordBattleDuration(durationMs: number): void {
    this.statsd.histogram('battle.duration', durationMs);
    this.statsd.increment('battle.count');
  }

  recordCacheHit(hit: boolean): void {
    this.statsd.increment(hit ? 'cache.hits' : 'cache.misses');
  }

  recordExternalApiCall(success: boolean, durationMs: number): void {
    this.statsd.histogram('external_api.duration', durationMs);
    this.statsd.increment(`external_api.${success ? 'success' : 'error'}`);
  }
}
