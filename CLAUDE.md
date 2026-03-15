# SRE Backend Arena — CLAUDE.md

## Visão Geral

Este repositório é um **desafio técnico de SRE** com três implementações de referência prontas para uso. Cada implementação resolve um dos três cenários do desafio usando uma stack diferente.

## Estrutura do Repositório

```
sre-backend-arena/
├── README.md                  # Regras do desafio e sistema de pontuação
├── FASTAPI.md                 # Guia completo da implementação FastAPI
├── KOTLIN.md                  # Guia completo da implementação Kotlin
├── NESTJS.md                  # Guia completo da implementação NestJS
├── sre-arena-deathstar/       # Projeto FastAPI — Cenário Star Wars
├── sre-arena-wizard/          # Projeto Kotlin — Cenário Harry Potter
└── sre-arena-pokemon/         # Projeto NestJS — Cenário Pokémon
```

## Projetos

### `sre-arena-deathstar/` — FastAPI + Star Wars
- **Endpoint:** `GET /deathstar-analysis/{shipId}`
- **Stack:** Python 3.11 + FastAPI + Uvicorn + Redis + aiohttp
- **API Externa:** SWAPI (`https://swapi.dev/api`) — limite: ~1000 req/hora
- **Porta:** 8000
- **Testes:** `pytest tests/ -v --cov=src`
- **Dev:** `make run` ou `make docker-run`

### `sre-arena-wizard/` — Kotlin + Harry Potter
- **Endpoint:** `GET /wizard/{name}`
- **Stack:** Kotlin + Ktor + Caffeine Cache + Resilience4j
- **API Externa:** PotterDB (`https://api.potterdb.com/v1`) — limite: 100 req/min
- **Porta:** 8080
- **Testes:** `./gradlew test`
- **Dev:** `docker-compose up -d`

### `sre-arena-pokemon/` — NestJS + Pokémon
- **Endpoint:** `GET /battle?pokemonA={name}&pokemonB={name}`
- **Stack:** Node.js 20 + NestJS + Fastify + Opossum (circuit breaker) + hot-shots (StatsD)
- **API Externa:** PokéAPI (`https://pokeapi.co/api/v2`) — limite: ~100 req/min
- **Porta:** 3000
- **Testes:** `npm run test:cov`
- **Dev:** `docker-compose up -d`

## Padrões Comuns a Todos os Projetos

Cada projeto implementa os mesmos padrões de SRE:

| Padrão | FastAPI | Kotlin | NestJS |
|--------|---------|--------|--------|
| Cache | Redis + TTL | Caffeine in-memory | Map in-memory |
| Circuit Breaker | Custom impl | Resilience4j | Opossum |
| Retry + Backoff | Decorator `@retry` | Resilience4j | Dentro do circuit breaker |
| Rate Limiting | `RateLimiter` class | Resilience4j Token Bucket | Sliding window manual |
| Observabilidade | Prometheus + Datadog + Jaeger | DogStatsD + Prometheus | StatsD (hot-shots) + dd-trace |
| Health Checks | `/api/health/live`, `/api/health/ready` | `/health/live`, `/health/ready` | `/health/live`, `/health/ready` |
| K8s | YAML + Terraform | YAML + Terraform | YAML + Terraform |
| CI/CD | GitHub Actions | GitHub Actions | GitHub Actions |

## Infraestrutura

Todos os projetos têm a mesma estrutura de IaC:

```
terraform/
├── k8s/          # Kubernetes via Terraform (provider + deployment)
└── datadog/      # Datadog via Terraform (SLO + dashboard + monitors + variables)
k8s/              # Manifests YAML (namespace, deployment, service, ingress, hpa)
.github/workflows/ci-cd.yml
```

## Regras do Desafio

- **Rate limit é gatekeeper** — violar = desclassificação
- **Qualidade de código é gatekeeper** — código ruim = desclassificação
- **Budget de recursos:** 1.5 CPU + 350MB RAM (local) / 2.0 CPU + 512MB RAM (cloud)
- **Mínimo 2 réplicas** em Kubernetes
- **Cobertura mínima de testes:** 70%
- **docker-compose** é apenas para desenvolvimento; entrega final deve ser K8s

## Guias de Referência

Para detalhes completos de cada implementação (código, configuração, decisões de design):
- FastAPI: ver [FASTAPI.md](FASTAPI.md)
- Kotlin: ver [KOTLIN.md](KOTLIN.md)
- NestJS: ver [NESTJS.md](NESTJS.md)
