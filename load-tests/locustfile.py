"""
SRE Backend Arena — Locust Load Test

Uso:
  # Web UI (recomendado)
  locust -f locustfile.py --host http://localhost:8000

  # Headless (CI/CD)
  locust -f locustfile.py \
    --host http://localhost:8000 \
    --users 200 --spawn-rate 20 \
    --run-time 60s --headless \
    --csv=results/deathstar

Selecione o cenário via variável de ambiente SCENARIO:
  SCENARIO=deathstar locust -f locustfile.py --host http://localhost:8000
  SCENARIO=wizard    locust -f locustfile.py --host http://localhost:8080
  SCENARIO=pokemon   locust -f locustfile.py --host http://localhost:3000

Valor padrão: SCENARIO=deathstar
"""

import os
import random

from locust import HttpUser, between, events, task

# ---------------------------------------------------------------------------
# Payloads por cenário
# ---------------------------------------------------------------------------

WIZARD_NAMES = [
    "harry-potter", "hermione-granger", "ron-weasley", "albus-dumbledore",
    "voldemort", "severus-snape", "draco-malfoy", "luna-lovegood",
    "neville-longbottom", "bellatrix-lestrange", "sirius-black",
    "remus-lupin", "minerva-mcgonagall", "rubeus-hagrid", "ginny-weasley",
]

SHIP_IDS = list(range(2, 37))  # SWAPI: naves de id 2 a 36

POKEMON_PAIRS = [
    ("pikachu", "charizard"), ("bulbasaur", "squirtle"), ("mewtwo", "mew"),
    ("gengar", "alakazam"), ("snorlax", "lapras"), ("dragonite", "gyarados"),
    ("raichu", "jolteon"), ("machamp", "golem"), ("arcanine", "rapidash"),
    ("vaporeon", "starmie"),
]

SCENARIO = os.getenv("SCENARIO", "deathstar").lower()

# ---------------------------------------------------------------------------
# User classes por cenário
# ---------------------------------------------------------------------------

class DeathstarUser(HttpUser):
    """Cenário Star Wars — GET /deathstar-analysis/{shipId}"""
    wait_time = between(0.05, 0.2)

    @task(10)
    def analyze_ship(self):
        ship_id = random.choice(SHIP_IDS)
        self.client.get(
            f"/deathstar-analysis/{ship_id}",
            name="/deathstar-analysis/[shipId]",
        )

    @task(1)
    def health_live(self):
        self.client.get("/api/health/live", name="/health/live")

    @task(1)
    def health_ready(self):
        self.client.get("/api/health/ready", name="/health/ready")


class WizardUser(HttpUser):
    """Cenário Harry Potter — GET /wizard/{name}"""
    wait_time = between(0.05, 0.2)

    @task(10)
    def get_wizard(self):
        name = random.choice(WIZARD_NAMES)
        self.client.get(f"/wizard/{name}", name="/wizard/[name]")

    @task(1)
    def health_live(self):
        self.client.get("/health/live", name="/health/live")

    @task(1)
    def health_ready(self):
        self.client.get("/health/ready", name="/health/ready")


class PokemonUser(HttpUser):
    """Cenário Pokémon — GET /battle?pokemonA={name}&pokemonB={name}"""
    wait_time = between(0.05, 0.2)

    @task(10)
    def battle(self):
        a, b = random.choice(POKEMON_PAIRS)
        self.client.get(
            f"/battle?pokemonA={a}&pokemonB={b}",
            name="/battle?pokemonA=[a]&pokemonB=[b]",
        )

    @task(1)
    def health_live(self):
        self.client.get("/health/live", name="/health/live")

    @task(1)
    def health_ready(self):
        self.client.get("/health/ready", name="/health/ready")


# ---------------------------------------------------------------------------
# Seleção dinâmica de User class via SCENARIO
# ---------------------------------------------------------------------------

_SCENARIO_MAP = {
    "deathstar": DeathstarUser,
    "wizard":    WizardUser,
    "pokemon":   PokemonUser,
}

if SCENARIO not in _SCENARIO_MAP:
    raise ValueError(
        f"SCENARIO inválido: '{SCENARIO}'. "
        f"Valores aceitos: {list(_SCENARIO_MAP.keys())}"
    )

# Desativa as classes não usadas para que o Locust não as registre
_active = _SCENARIO_MAP[SCENARIO]
for _cls in list(_SCENARIO_MAP.values()):
    if _cls is not _active:
        _cls.abstract = True

# ---------------------------------------------------------------------------
# Hooks: banner de início e relatório de critérios ao fim do teste
# ---------------------------------------------------------------------------

PASS = "\033[92m✔\033[0m"
FAIL = "\033[91m✘\033[0m"
SEP  = "─" * 60


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print(f"\n  SRE Backend Arena — Locust")
    print(f"  Cenário : {SCENARIO}")
    print(f"  Host    : {environment.host}\n")


@events.quitting.add_listener
def on_quitting(environment, **kwargs):
    stats      = environment.stats.total
    rps        = stats.current_rps
    p99_ms     = stats.get_response_time_percentile(0.99) or 0
    failures   = stats.num_failures
    requests   = stats.num_requests

    print(f"\n{SEP}")
    print(f"  RELATÓRIO DE CARGA — {SCENARIO.upper()}")
    print(SEP)
    print(f"\n  Requisições  : {requests:>10,}")
    print(f"  Throughput   : {rps:>10,.1f} RPS")
    print(f"  Falhas       : {failures:>10,}")
    print(f"  p99 latência : {p99_ms:>10.1f} ms")

    print(f"\n  ── Critérios do Desafio ────────────────────────")

    def chk(label: str, passed: bool, detail: str = ""):
        icon = PASS if passed else FAIL
        suffix = f"  ({detail})" if detail else ""
        print(f"  {icon} {label}{suffix}")

    chk("Throughput ≥ 8.000 RPS  (+20 pts)", rps >= 8_000,  f"{rps:,.0f} RPS")
    chk("Throughput ≥ 10.000 RPS (+25 pts)", rps >= 10_000, f"{rps:,.0f} RPS")
    chk("Latência p99 < 300ms    (+10 pts)", p99_ms < 300,  f"{p99_ms:.1f} ms")
    chk("Latência p99 < 150ms    (+15 pts)", p99_ms < 150,  f"{p99_ms:.1f} ms")
    chk("Zero erros 5xx          (+5 pts)",  failures == 0,  f"{failures} erros")

    print(f"\n{SEP}\n")
