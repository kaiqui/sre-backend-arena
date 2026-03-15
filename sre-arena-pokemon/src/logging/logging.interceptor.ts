import {
  Injectable,
  NestInterceptor,
  ExecutionContext,
  CallHandler,
  Logger,
} from '@nestjs/common';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { v4 as uuidv4 } from 'uuid';

@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  private readonly logger = new Logger('HTTP');

  intercept(context: ExecutionContext, next: CallHandler): Observable<unknown> {
    const req = context.switchToHttp().getRequest();
    const traceId = req.headers['x-trace-id'] || uuidv4();
    const { method, url } = req;
    const start = Date.now();

    return next.handle().pipe(
      tap({
        next: () => {
          const duration = Date.now() - start;
          this.logger.log({ message: `${method} ${url}`, traceId, duration, status: 'success' });
        },
        error: (err) => {
          const duration = Date.now() - start;
          this.logger.error({ message: `${method} ${url}`, traceId, duration, status: 'error', error: err.message });
        },
      }),
    );
  }
}
