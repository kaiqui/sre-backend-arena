# 🏆 SRE Backend Arena — Reliability Challenge

> *"Não basta funcionar. Precisa ser observável, confiável e eficiente — sob pressão."*

Um desafio técnico para avaliar **engenharia de software + práticas de SRE** em cenário de alta concorrência. Foco em **Datadog** para observabilidade, **Terraform** para Infrastructure as Code, e sistema de pontuação competitivo.

---

## 🎮 Como Funciona a Competição

Cada candidato constrói uma solução que será testada sob carga extrema. A pontuação final combina **performance técnica + confiabilidade + observabilidade + IaC**, com bônus por conquistas especiais.

```
🏆 PONTUAÇÃO FINAL = 
   [Performance: 35%] + 
   [Confiabilidade: 25%] + 
   [Observabilidade Datadog: 20%] + 
   [Infrastructure as Code: 10%] + 
   [Achievements: +10% bônus]
```

---

## ⏱️ Prazo

**7 dias corridos** a partir do início do desafio.

---

## 🎯 Objetivo do Desafio

Construir **um serviço HTTP com um endpoint** que integre com APIs públicas e responda com formato pré-definido, suportando:

```
🔥 10.000 requisições por segundo (RPS)
🔥 APIs externas com latência variável e falhas intermitentes
🔥 Resource budget rígido: 1.5 CPU + 350MB RAM (TODA a stack)
🔥 Rate limits das APIs externas DEVEM ser respeitados
🔥 Infraestrutura e Observabilidade como Código
```

---

## 🏗️ Requisitos de Infraestrutura

### Ambiente de Execução

| Ambiente | Requisito |
|----------|-----------|
| **Cloud** | Kubernetes gerenciado (EKS, GKE, AKS) ou serviços gerenciados (ECS, Cloud Run, Container Apps) |
| **Local** | Kubernetes local obrigatório (kind, k3d, minikube) |

> ⚠️ **docker-compose não é aceito para entrega final**. Apenas para desenvolvimento local.

### Arquitetura Mínima

- Load Balancer configurado
- Mínimo 2 réplicas da aplicação
- Health checks (liveness e readiness)
- Resource limits definidos em todos os containers
- Namespace dedicado para isolamento

---

## 🧭 Cenários Disponíveis (Escolha APENAS 1)

> ⚠️ Para ranking justo, todos os candidatos no mesmo cenário são comparados diretamente.

---

### 🔮 Cenário 1 — Wizard Intelligence Network (Harry Potter)

#### 📖 A História

**Ano de 1997.** A Segunda Guerra Bruxa está em seu ápice. A Ordem da Fênix opera nas sombras, mas precisa de inteligência rápida sobre bruxos das trevas para proteger aliados e planejar operações.

O **Ministério da Magia** foi infiltrado por Comensais da Morte. Os registros tradicionais não são confiáveis. A Ordem precisa de um sistema **descentralizado, rápido e resiliente** que possa:

- Identificar rapidamente a lealdade de um bruxo
- Calcular seu nível de poder mágico para avaliar ameaças
- Funcionar mesmo quando as fontes de inteligência (APIs externas) estiverem comprometidas

Você foi recrutado por **Alastor "Olho-Tonto" Moody** para construir este sistema. A vida de membros da Ordem pode depender da velocidade e confiabilidade das suas respostas.

*"Constante Vigilância!"* — e seu sistema precisa ser a personificação disso.

#### 🎯 Missão Técnica

```
GET /wizard/{name}
```

**Resposta Esperada:**
```json
{
  "name": "Harry Potter",
  "house": "Gryffindor",
  "species": "human",
  "wizard": true,
  "powerScore": 87
}
```

#### ⚠️ Rate Limit da API
| API | Rate Limit |
|-----|------------|
| The Harry Potter API | **100 requests/min** |

> 🚨 **Violar o rate limit = Desclassificação**

---

### 🚀 Cenário 2 — Death Star Threat Analysis (Star Wars)

#### 📖 A História

**Ano 0 ABY.** A Aliança Rebelde interceptou transmissões imperiais sobre movimentação de naves capital. A **Estrela da Morte** foi detectada, mas inteligência incompleta coloca todas as bases rebeldes em risco.

A **Princesa Leia** precisa de um sistema que possa:

- Analisar rapidamente qualquer nave imperial identificada
- Calcular nível de ameaça baseado em múltiplos fatores (tripulação, armamento, classe)
- Funcionar sob carga extrema quando múltiplas células rebeldes consultarem simultaneamente
- Continuar operando mesmo quando os satélites de inteligência (APIs externas) forem bloqueados pelo Império

Você foi designado pelo **Comando Rebelde** para construir esta ferramenta. O sucesso do ataque à Estrela da Morte depende da qualidade da inteligência que você entregar.

*"Que a Força esteja com você."* — e com a resiliência do seu sistema.

#### 🎯 Missão Técnica

```
GET /deathstar-analysis/{shipId}
```

**Resposta Esperada:**
```json
{
  "ship": "Death Star",
  "model": "DS-1 Orbital Battle Station",
  "crew": 342953,
  "passengers": 843342,
  "threatScore": 98,
  "classification": "galactic_superweapon"
}
```

#### ⚠️ Rate Limit da API
| API | Rate Limit |
|-----|------------|
| SWAPI | **~1000 requests/hour** |

> 🚨 **Violar o rate limit = Desclassificação**

---

### ⚔️ Cenário 3 — Pokémon Battle Arena (Pokémon)

#### 📖 A História

**Ano 2024.** A **Liga Pokémon Mundial** está realizando o primeiro campeonato totalmente automatizado. Milhões de espectadores assistem via streaming enquanto batalhas são simuladas em tempo real para entretenimento e análise estratégica.

A **Plataforma de E-Sports** precisa de um serviço que possa:

- Simular batalhas entre quaisquer dois Pokémon instantaneamente
- Calcular o vencedor baseado em stats reais (HP, Attack, Defense, Speed)
- Suportar picos de audiência durante finais de campeonato (10k+ batalhas/segundo)
- Continuar operando mesmo quando a PokéAPI estiver sobrecarregada

Você foi contratado pela **Liga Pokémon** para construir o motor de simulação. A credibilidade do campeonato e a experiência de milhões de fãs dependem da sua solução.

*"Gotta Catch 'Em All!"* — e garantir que todas as batalhas sejam justas e rápidas.

#### 🎯 Missão Técnica

```
GET /battle?pokemonA={name}&pokemonB={name}
```

**Resposta Esperada:**
```json
{
  "pokemonA": "pikachu",
  "pokemonB": "charizard",
  "winner": "charizard",
  "reason": "higher_total_stats"
}
```

#### ⚠️ Rate Limit da API
| API | Rate Limit |
|-----|------------|
| PokéAPI | **~100 requests/min** |

> 🚨 **Violar o rate limit = Desclassificação**

---

## 📊 Sistema de Pontuação

### 🏁 Performance (35 pontos)

| Métrica | Pontos |
|---------|--------|
| Throughput ≥ 8k RPS | 20 |
| Throughput ≥ 10k RPS | 25 |
| Latência p99 < 300ms | 10 |
| Latência p99 < 150ms | 15 |
| Zero erros 5xx sob carga | 5 |

### 🛡️ Confiabilidade (25 pontos)

| Prática | Pontos |
|---------|--------|
| Retry com backoff exponencial | 8 |
| Timeout em calls externas | 7 |
| Cache com TTL | 8 |
| Circuit breaker ou fallback | 7 |
| Rate limit client-side | +5 bônus |

### 📈 Observabilidade Datadog (20 pontos)

| Item | Pontos |
|------|--------|
| Agent configurado + métricas customizadas | 8 |
| Logs estruturados com trace_id | 5 |
| SLO + monitores configurados | 5 |
| Datadog via Terraform | +5 bônus |

### 🏗️ Infrastructure as Code (10 pontos)

| Prática | Pontos |
|---------|--------|
| Manifestos K8s versionados | 5 |
| K8s via Terraform | +5 bônus |
| Datadog via Terraform | +5 bônus |
| Remote state gerenciado | +3 bônus |
| Terraform plan limpo | +2 bônus |

### 🎁 Achievements (até +10 pontos bônus)

| Conquista | Pontos |
|-----------|--------|
| Chaos Survivor | 3 |
| Cost Whisperer | 3 |
| Trace Master | 2 |
| SLO Guardian | 2 |
| Rate Limit Guardian | 2 |
| Terraform Wizard | 3 |

---

## 🔧 Resource Budget

| Ambiente | CPU Total | Memória Total |
|----------|-----------|---------------|
| Cloud K8s | 2.0 cores | 512MB |
| Local K8s | 1.5 cores | 350MB |

> ⚠️ Exceder o budget = **desclassificação**

---

## 📡 Requisitos de Observabilidade

### Obrigatório

- Métricas customizadas enviadas ao Datadog
- Logs estruturados em JSON com correlation ID
- Health checks com dependências
- SLO definido e monitorado

### Entregáveis

- Dashboards como código
- SLOs como código
- Alertas/monitores como código
- Instrumentação da aplicação

---

## 🔄 CI/CD

Pipeline automatizada deve executar:

- Lint
- Testes (mínimo 70% coverage)
- Build
- Validação de IaC
- Deploy

---

## 📦 Entrega

O candidato deve enviar:

1. Link do repositório público
2. URL pública da API ou instruções de deploy local
3. Acesso ao Datadog (read-only) ou evidências dos dashboards/SLOs
4. Documentação de arquitetura explicando:
   - Decisões de design
   - Estratégia de cache/retry/fallback
   - Como os rate limits são respeitados
   - Escolhas de IaC
5. Lista de achievements desbloqueados
6. Evidências de compliance com rate limits

---

## 🏆 Critérios de Avaliação

| Categoria | Peso | Gatekeeper |
|-----------|------|------------|
| Performance | 35% | Não |
| Confiabilidade | 25% | Não |
| Observabilidade | 20% | Não |
| Infrastructure as Code | 10% | Não |
| Achievements | +10% bônus | Não |
| Qualidade de Código | — | **Sim** |
| Rate Limit Compliance | — | **Sim** |

> ⚠️ **Qualidade de código insuficiente ou violação de rate limit = desclassificação automática**

---

## ❓ FAQ

**P: Posso usar YAML para K8s em vez de Terraform?**  
R: Sim. Terraform é opcional mas pontua mais.

**P: Posso usar dashboard.json em vez de Terraform para Datadog?**  
R: Pode, mas Terraform para Datadog dá pontos extras.

**P: docker-compose é aceito?**  
R: Apenas para desenvolvimento. Entrega final deve ser K8s ou serviços gerenciados.

**P: Como provo que respeitei os rate limits?**  
R: Métricas e logs mostrando zero violações durante o teste de carga.

**P: Preciso usar remote state para Terraform?**  
R: Não é obrigatório, mas dá pontos extras.

---

## 📋 Checklist de Submissão

```
[ ] Repositório público com código completo
[ ] Infraestrutura como código (YAML ou Terraform)
[ ] Dockerfile funcional
[ ] Datadog instrumentado (métricas + logs + traces)
[ ] SLO + Dashboard + Alertas como código
[ ] Tests com ≥70% coverage
[ ] CI/CD pipeline configurada
[ ] Rate limiting client-side implementado
[ ] Documentação de arquitetura
[ ] Lista de achievements declarada
```

---

> 💡 **Dica Final**:  
> *"SRE não é sobre evitar falhas. É sobre construir sistemas que continuam funcionando — e te avisando — quando elas acontecem."*

---

**Pronto para entrar na Arena?** 🥊

🚀 **Boa sorte, engenheiro(a) de confiabilidade!**