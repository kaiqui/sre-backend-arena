.PHONY: up down logs ps build warm test-load stats

# ─────────────────────────────────────────────────────────────────────────────
# Stack
# ─────────────────────────────────────────────────────────────────────────────

up:          ## Sobe a stack com 2 réplicas da app + nginx
	docker compose up --build -d
	@echo ""
	@echo "  Aguardando healthchecks..."
	@docker compose ps --wait 2>/dev/null || sleep 20
	@echo ""
	@echo "  ✔  Stack pronta em http://localhost:8000"
	@echo "  ✔  Health: http://localhost:8000/health/live"
	@echo ""
	@echo "  Execute 'make warm' para aquecer o cache antes do load test."

down:        ## Para e remove todos os containers
	docker compose down --remove-orphans

logs:        ## Segue logs de todos os serviços
	docker compose logs -f

ps:          ## Status dos containers e uso de recursos
	docker compose ps
	@echo ""
	docker stats --no-stream $$(docker compose ps -q)

build:       ## Reconstrói as imagens sem subir
	docker compose build --no-cache

# ─────────────────────────────────────────────────────────────────────────────
# Cache warm-up
# Dispara 1 req para cada ship ID (2–36) em ambas as réplicas.
# Após isso o cache está quente e as 10K RPS viram 100% hits.
# ─────────────────────────────────────────────────────────────────────────────

warm:        ## Aquece o cache — bate nos 35 ship IDs 2x (uma por réplica)
	@echo "  Aquecendo cache (35 ships × 2 rounds)..."
	@for round in 1 2; do \
	  for id in $$(seq 2 36); do \
	    curl -sf http://localhost:8000/deathstar-analysis/$$id -o /dev/null & \
	  done; \
	  wait; \
	  echo "  round $$round concluído"; \
	done
	@echo "  ✔  Cache aquecido!"

# ─────────────────────────────────────────────────────────────────────────────
# Load test (chama o locustfile.py do diretório load-tests/)
# ─────────────────────────────────────────────────────────────────────────────

USERS    ?= 200
SPAWN    ?= 20
DURATION ?= 60s
LOAD_DIR  = ../load-tests

test-load:   ## Roda o Locust headless contra a stack local
	@echo "  Iniciando load test: $(USERS) VUs, spawn $(SPAWN)/s, $(DURATION)"
	cd $(LOAD_DIR) && \
	SCENARIO=deathstar poetry run locust -f locustfile.py \
	  --host http://localhost:8000 \
	  --users $(USERS) --spawn-rate $(SPAWN) \
	  --run-time $(DURATION) --headless \
	  --csv=results/deathstar \
	  --html=results/deathstar.html
	@echo "  Relatório salvo em $(LOAD_DIR)/results/deathstar.html"

# ─────────────────────────────────────────────────────────────────────────────
# Testes unitários (dentro do container para isolar ambiente)
# ─────────────────────────────────────────────────────────────────────────────

test:        ## Roda pytest com cobertura
	docker compose run --rm --no-deps app \
	  sh -c "pip install pytest pytest-cov pytest-asyncio --quiet && \
	         pytest tests/ -v --cov=src --cov-report=term-missing"

help:        ## Lista todos os targets
	@grep -E '^[a-zA-Z_-]+:.*?##' Makefile | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'
