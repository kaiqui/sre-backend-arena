import { Controller, Get } from '@nestjs/common';

@Controller('health')
export class HealthController {
  @Get('live')
  liveness() {
    return { status: 'alive' };
  }

  @Get('ready')
  readiness() {
    return { status: 'ready' };
  }
}
