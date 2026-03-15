import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { BattleModule } from './battle/battle.module';
import { HealthModule } from './health/health.module';
import { MetricsModule } from './metrics/metrics.module';
import configSchema from './config/schema';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      validationSchema: configSchema,
    }),
    BattleModule,
    HealthModule,
    MetricsModule,
  ],
})
export class AppModule {}
