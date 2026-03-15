import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

interface CacheEntry<T> {
  value: T;
  expiresAt: number;
}

@Injectable()
export class CacheService {
  private readonly logger = new Logger(CacheService.name);
  private readonly store = new Map<string, CacheEntry<unknown>>();
  private readonly ttlMs: number;
  private hits = 0;
  private misses = 0;

  constructor(private readonly config: ConfigService) {
    this.ttlMs = this.config.get<number>('CACHE_TTL_MS', 86400000);
  }

  get<T>(key: string): T | null {
    const entry = this.store.get(key);
    if (!entry || Date.now() > entry.expiresAt) {
      if (entry) this.store.delete(key);
      this.misses++;
      return null;
    }
    this.hits++;
    return entry.value as T;
  }

  set<T>(key: string, value: T, ttlMs?: number): void {
    this.store.set(key, {
      value,
      expiresAt: Date.now() + (ttlMs ?? this.ttlMs),
    });
  }

  getStats() {
    return { hits: this.hits, misses: this.misses, size: this.store.size };
  }
}
