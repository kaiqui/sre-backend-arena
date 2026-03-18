.PHONY: install deathstar wizard pokemon deathstar-ui wizard-ui pokemon-ui clean

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

install:
	poetry install

# ---------------------------------------------------------------------------
# Headless — 200 VUs, spawn 20/s, 60s
# Sobrescreva com: make deathstar USERS=500 SPAWN=50 DURATION=120s
# ---------------------------------------------------------------------------

USERS    ?= 200
SPAWN    ?= 20
DURATION ?= 60s

deathstar:
	SCENARIO=deathstar poetry run locust -f locustfile.py \
		--host http://localhost:8000 \
		--users $(USERS) --spawn-rate $(SPAWN) \
		--run-time $(DURATION) --headless \
		--csv=results/deathstar \
		--html=results/deathstar.html

wizard:
	SCENARIO=wizard poetry run locust -f locustfile.py \
		--host http://localhost:8080 \
		--users $(USERS) --spawn-rate $(SPAWN) \
		--run-time $(DURATION) --headless \
		--csv=results/wizard \
		--html=results/wizard.html

pokemon:
	SCENARIO=pokemon poetry run locust -f locustfile.py \
		--host http://localhost:3000 \
		--users $(USERS) --spawn-rate $(SPAWN) \
		--run-time $(DURATION) --headless \
		--csv=results/pokemon \
		--html=results/pokemon.html

# ---------------------------------------------------------------------------
# Web UI — abre em http://localhost:8089
# ---------------------------------------------------------------------------

deathstar-ui:
	SCENARIO=deathstar poetry run locust -f locustfile.py \
		--host http://localhost:8000

wizard-ui:
	SCENARIO=wizard poetry run locust -f locustfile.py \
		--host http://localhost:8080

pokemon-ui:
	SCENARIO=pokemon poetry run locust -f locustfile.py \
		--host http://localhost:3000

# ---------------------------------------------------------------------------
# Limpa resultados gerados
# ---------------------------------------------------------------------------

clean:
	rm -f results/*.csv results/*.html
