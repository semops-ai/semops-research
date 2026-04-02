# Mirror Architecture Generation — User Guide

Build a complete business architecture and DDD mirror for any company from minimal inputs. The pipeline derives strategic decisions (what should exist), then mechanically renders them as architectural components (bounded contexts, schema, manifests, analytics patterns).

## What This Does

The pipeline has two 1P patterns, each with distinct capabilities:

### Business Architecture (strategic decisions — what should exist)

| Command | Capability | Artifact |
|---------|-----------|----------|
| `/classify` | `business-classification` | `classification.yaml` |
| `/decompose-business-model` | `business-model-decomposition` | archetype catalog YAMLs |
| `/predict` | `reference-model-prediction` | `reference-model.yaml` |
| `/synthesize` | `business-model-synthesis` | `business-model.yaml` |

### Business Architecture → DDD Derivation (structural components — rendering decisions)

| Command | Capability | Artifact |
|---------|-----------|----------|
| `/derive` | `agentic-ddd-derivation` | `STRATEGIC_DDD.md`, `UBIQUITOUS_LANGUAGE.md`, `ARCHITECTURE.md`, `INFRASTRUCTURE.md`, `system-inventory.yaml`, `system-classification.yaml` |
| `/derive-schema` | `schema-derivation` | `schema.sql` |
| `/derive-manifests` | `manifest-derivation` | bronze/silver/gold/governance layer YAMLs |
| `/derive-analytics` | `analytics-derivation` | per-context analytics pattern files |
| `/derive-registry` | `registry-derivation` | per-engagement `registry.yaml` |
| `/process-analysis` | `process-analysis` | process catalog YAMLs + capability inventory |
| `/decompose-vendor` | `vendor-decomposition` | vendor decomposition YAML |

### Observation + Convergence (bottom-up validation)

| Command | What |
|---------|------|
| `/observe` | Collect signals from public sources (OSINT) |
| `/diagnose` | Gap analysis — predicted vs. observed → TOGAF ADM gap classification |

**Framework lineage:** BIZBOK (content) → `business-architecture` (1P strategic) → `busarch-ddd-derivation` (1P structural) ← DDD (vocabulary). TOGAF provides the method (gap analysis, phase structure). APQC, DCAM, DAMA provide additional content for specific dimensions.

**Two scenarios:**

1. **Consulting engagement** — walking into a company cold, build the architecture before the first meeting
2. **PE due diligence** — evaluating a target's data maturity before acquisition

## Quick Start

```text
# 1. Classify the target company
/classify EDGE Cleaning Services

# 2. Build archetype catalog (if thin coverage for this business model)
/decompose-business-model field-service-recurring

# 3. Generate reference model (what should exist)
/predict

# 4. Synthesize (investment thesis, domain typing, merge decisions)
/synthesize

# 5. Derive full DDD architecture
/derive

# 6. Generate structural components
/derive-schema
/derive-manifests
/derive-analytics
/derive-registry

# 7. Process analysis (capabilities, cognitive load, automation opportunities)
/process-analysis

# 8. Vendor decomposition (if using a platform like Jobber, Shopify, etc.)
/decompose-vendor Jobber
```

Each command produces structured artifacts in the engagement mirror directory. The reasoning logs go to `docs/engagement-logs/` in semops-research.

## Classification Fields

The `Classification` is the single input. Fill in what you know — the engine handles missing fields with conservative defaults.

| Field | Required | Example | Notes |
|-------|----------|---------|-------|
| `customer_type` | Yes | `"b2b"`, `"b2c"`, `"b2b2c"` | Who buys from this company |
| `sector` | Yes | `"enterprise_software"` | Broad sector |
| `industry` | Yes | `"vertical_saas"`, `"trade_shows"` | Specific industry (drives entity predictions) |
| `vertical` | No | `"logistics"`, `"audio_hifi"` | Domain niche (captured but not yet used for predictions — see []) |
| `geography` | No | `"global"`, `"regional"` | Defaults to `"global"` |
| `business_model` | No | `["subscription", "usage_based"]` | Revenue model(s) — layers additional entities |
| `service_model` | No | `"saas"`, `"on_prem"` | Delivery model |
| `revenue_range` | No | `"$20M-$50M"` | Drives scale-dependent predictions |
| `employee_count` | No | `200` | Additional scale signal |
| `metadata` | No | `{"product_domains": ["ml_ai"]}` | Extensible — `product_domains` adds domain entities |

### Industry Keys

These industry values have dedicated entity sets in YAML catalogs (`data/catalogs/industries/`):

| Key | Example Companies |
|-----|-------------------|
| `vertical_saas` | Veeva, Procore, Toast |
| `horizontal_saas` | Slack, Notion, Monday |
| `cloud_platform` | AWS, GCP, Azure |
| `financial_services` | Goldman, Stripe, Square |
| `insurance` | Lemonade, Root, Oscar |
| `healthcare` | Epic, Cerner, Athena |
| `manufacturing` | Siemens, Rockwell, Honeywell |
| `telecommunications` | T-Mobile, Comcast, AT&T |
| `transportation` | FedEx, Uber Freight, Flexport |
| `retail` | Shopify merchants, Target, Walmart |
| `marketplace` | Airbnb, Etsy, eBay |
| `events` | Generic conferences, festivals, meetups |
| `trade_shows` | , CES, NRF, HIMSS |

Industries not in this list fall through to universal entities + business model entities + process-implied entities. The engine still produces useful output — just less industry-specific.

### Business Model Keys

These layer additional entities on top of the industry set:

| Key | Entities Added |
|-----|---------------|
| `subscription` | Subscription, Plan, BillingCycle, Renewal, Churn |
| `usage_based` | UsageRecord, UsageMetric, RatingRule |
| `transactional` | Order, OrderItem, Cart |
| `marketplace` | Listing, Commission |
| `advertising` | AdImpression, Campaign, AdPlacement |
| `freemium` | Trial, ConversionEvent |
| `licensing` | License, LicenseKey, Entitlement |

### Revenue Range Values

The engine normalizes free-form revenue strings. These all work:

```
"<$5M", "$5M-$20M", "$20M-$50M", "$50M-$100M", "$100M+", "$200M+", "$1B+"
```

If omitted, defaults to the most conservative scale (`<$5M`).

### Product Domains

Pass via `metadata={"product_domains": [...]}` to layer domain-specific entities:

```
"search", "discovery", "personalization", "analytics_bi", "ml_ai",
"data_platform", "payments_commerce", "identity_auth", "video_streaming",
"publishing", "voice_conversational"
```

## The 7 Prediction Dimensions

`generate_reference` returns a `ReferenceModel` with predictions across 7 dimensions:

### 1. System Mix

Predicts the ratio of four data system types (from the data-system-classification framework):

- **Application** — systems that run the product (SaaS apps, APIs)
- **Analytics** — systems that measure and analyze (BI, data warehouse)
- **Work** — systems that coordinate people and processes (project management, CRM)
- **Record** — systems of record (ERP, financial systems, HR)

```python
ref.system_mix.application  # 0.60 for SaaS
ref.system_mix.analytics    # 0.25
ref.system_mix.work         # 0.10
ref.system_mix.record       # 0.05
ref.system_mix.business_type  # "software_saas"
```

**Business type profiles:**

| Type | App | Analytics | Work | Record | Best For |
|------|-----|-----------|------|--------|----------|
| `software_saas` | 60% | 25% | 10% | 5% | SaaS companies |
| `traditional_enterprise` | 30% | 20% | 10% | 40% | Manufacturing, financial services |
| `professional_services` | 15% | 5% | 50% | 30% | Consulting, legal, accounting |
| `consumer_tech` | 20% | 70% | 10% | 0% | Streaming, social, consumer apps |
| `events_project` | 20% | 15% | 40% | 25% | Trade shows, conferences, events |

### 2. Entities

Predicted canonical entities the company should have, layered from multiple sources:

```python
for entity in ref.entities:
    print(f"{entity.name} [{entity.category}] conf={entity.confidence}")
    # Customer [core] conf=0.9
    # Subscription [core] conf=0.8
    # Strategy [process-implied] conf=0.6
```

**Layering order** (first source wins, deduplicates by name):

1. **Universal** (conf 0.9) — Customer, Employee, Product, Contract, Account
2. **Industry** (conf 0.8) — from `ENTITIES_BY_INDUSTRY[industry]`
3. **Business model** (conf 0.8) — from `ENTITIES_BY_BUSINESS_MODEL[model]`
4. **Product domain** (conf 0.7) — from `ENTITIES_BY_PRODUCT_DOMAIN[domain]`
5. **Process-implied** (conf 0.6) — from APQC operating process categories

**Confidence is diagnostic:** High-confidence entities (0.8+) should definitely exist. Low-confidence process-implied entities (0.6) may or may not apply — compare against observed signals.

### 3. Processes

Expected business process categories from APQC Process Classification Framework:

```python
for process in ref.processes:
    print(f"{process.pcf_category} {process.name}")
    # 1.0 Develop Vision and Strategy
    # 6.0 Manage Customer Service
    # 7.0 Develop and Manage Human Capital
```

- **Operating processes** (1.0–6.0) — always included
- **Support processes** (7.0–13.0) — scale-dependent (small companies need HR + Finance; large companies need all 7)

### 4. Capabilities

Expected data management maturity from DCAM + DAMA-DMBOK:

```python
for cap in ref.capabilities:
    print(f"{cap.component} → {cap.expected_maturity} ({cap.framework_source})")
    # Data Strategy → Level 2-3: Developmental/Defined (dcam)
    # Data Architecture → Present (dama-dmbok)
```

- **DCAM** (8 components) — maturity level scales with revenue
- **DAMA** (11 knowledge areas) — which areas should be "Present" scales with revenue

### 5. Analytics

Expected analytics capabilities by business function:

```python
for a in ref.analytics:
    print(f"{a.function}: table_stakes={a.table_stakes}")
    print(f"  RED FLAG if missing: {a.red_flag_if_missing}")
```

Four functions: `bi`, `product`, `marketing`, `customer` — each with table_stakes, mature, and red_flag expectations.

### 6. Neutral Capabilities

Expected data platform capabilities (infrastructure-level):

```python
for nc in ref.neutral_capabilities:
    status = nc.expected_complexity if nc.expected_at_scale else "not expected"
    print(f"{nc.capability} → {status}")
    # Ingestion & Streaming → full
    # AI / ML Services → full
```

Seven capabilities: Ingestion & Streaming, Raw Storage, Table Layer, Analytic Engine, Orchestration & Pipelines, Governance & Catalog, AI / ML Services.

### 7. Team

Expected data team structure:

```python
print(f"Headcount: {ref.team.expected_headcount}")
print(f"Roles: {ref.team.expected_roles}")
print(f"Signal if missing: {ref.team.signal_if_missing}")
```

## How to Use for Diligence

### Step 1: Classify

Gather minimal business inputs from public sources (website, LinkedIn, job postings):

```text
/classify 
```

Produces `classification.yaml` with: industry (BIZBOK operational DNA), sector (NAICS), vertical, business model weights, engagement depth (tech_light/tech_heavy), and confidence levels per field.

### Step 2: Build Catalogs (if needed)

If the archetype catalog doesn't cover this business model:

```text
/decompose-business-model trade-show-event
```

Produces a structured catalog entry with capabilities, system mix baseline, cross-domain patterns.

### Step 3: Predict (top-down)

```text
/predict
```

Generates `reference-model.yaml` with predictions across 7 dimensions using the 5-layer entity prediction stack (see below). This is the "what should exist" for this type of company.

### Step 4: Synthesize

```text
/synthesize
```

The intelligence step — produces `business-model.yaml` with: investment thesis, domain type decisions (CORE/SUPPORTING/GENERIC with economic justification), merge decisions that challenge BIZBOK boundaries, cross-domain pattern resolution.

### Step 5: Derive Architecture

```text
/derive
```

Mechanical DDD derivation from synthesis output. Produces bounded contexts, aggregate roots, context map, domain events, sagas, plus initial `ARCHITECTURE.md` and `INFRASTRUCTURE.md`.

### Step 6: Generate Structural Components

```text
/derive-schema          # PostgreSQL schema per bounded context
/derive-manifests       # Bronze/silver/gold/governance layer definitions
/derive-analytics       # Per-context analytics patterns with metrics
/derive-registry        # Pattern + capability registry for this engagement
/process-analysis       # Process catalogs with cognitive load + automation assessment
/decompose-vendor Jobber  # Vendor product → neutral primitives (if applicable)
```

### Step 7: Observe (bottom-up)

Collect signals from public sources to validate predictions:

```text
/observe
```

See [CORPUS_COLLECTION.md](CORPUS_COLLECTION.md) for the full observe-side guide.

### Step 8: Diagnose (gap analysis)

Compare predictions to observations using TOGAF ADM gap classification:

```text
/diagnose
```

Every deviation between prediction and reality is diagnostic:

| Pattern | What It Means |
|---------|---------------|
| **Predicted entity missing** | Gap — company hasn't built this yet, or it's buried in spreadsheets |
| **Unexpected entity present** | Either novel innovation or legacy complexity |
| **Capability below expected maturity** | Underinvestment in data infrastructure |
| **Capability above expected maturity** | Either strong data culture or over-engineering |
| **Team smaller than expected** | Data work is distributed (risky) or outsourced |
| **Team larger than expected** | Heavy data investment — validate ROI |

## Engagement Persistence

Each engagement gets its own mirror directory with structured artifacts:

```text
outside-in/
  classification.yaml       # /classify output
  reference-model.yaml      # /predict output
  business-model.yaml       # /synthesize output
mirror/
  STRATEGIC_DDD.md          # /derive output
  UBIQUITOUS_LANGUAGE.md    # /derive output
  ARCHITECTURE.md           # /derive output (initial scaffold)
  INFRASTRUCTURE.md         # /derive output (initial scaffold)
  system-inventory.yaml     # /derive output
  system-classification.yaml # /derive output
  schema.sql                # /derive-schema output
  registry.yaml             # /derive-registry output
  domain/
    manifests/              # /derive-manifests output
    patterns/analytics/     # /derive-analytics output
```

Reasoning logs go to `docs/engagement-logs/<company>/` in semops-research.

## Known Limitations

1. **Vertical differentiation** — The `vertical` field is captured but doesn't influence predictions. Two trade shows in different domains (audio vs pet) produce identical reference models. See [] for planned LLM-augmented enrichment.

2. **Analytics expectations are SaaS-biased** — The analytics dimension was built from SaaS-centric research. Non-SaaS industries (events, manufacturing) get generic analytics expectations.

3. **No industry for your company?** — Industries not in the catalogs fall through to universal + business model + process-implied entities. The output is still useful, just less specific. Adding a new industry requires creating a YAML file in `data/catalogs/industries/`.

4. **YAML catalog coverage** — Framework data lives in YAML catalogs under `data/catalogs/` (industries, business models, product domains, processes, frameworks, operational). Industries not covered fall back to universal entities + business model + process-implied entities.

## 3P Framework Sources

All catalog data is derived from established frameworks:

| Framework | What It Provides | Source Doc |
|-----------|-----------------|------------|
| BIZBOK (Business Architecture Guild) | Entity prediction by industry | `docs/research/bizbok-reference-models.md` |
| APQC PCF (Process Classification Framework) | Process taxonomy, process-implied entities | `docs/research/apqc-process-framework.md` |
| DCAM (EDM Council) | Data management capability maturity | `docs/research/dcam-framework.md` |
| DAMA-DMBOK | Data management knowledge areas | `docs/research/dama-dmbok-overview.md` |
| Data System Classification | System mix profiles | `docs/research/data-system-classification.md` |
| Business Analytics Patterns | Analytics expectations by function + scale | `docs/research/business-analytics-patterns.md` |
| Data Systems Vendor Comparison | Neutral platform capabilities | `docs/research/data-systems-vendor-comparison.md` |
| Data Due Diligence Method | Team structure, diagnostic method | `docs/research/data-due-diligence-method.md` |

## Source Files

| File | What |
|------|------|
| `src/.../diligence/models.py` | All dataclasses (Classification, ReferenceModel, 7 dimension models) |
| `src/.../diligence/lookups.py` | Loads 15 framework tables from YAML catalogs (`data/catalogs/`) |
| `src/.../diligence/reference.py` | `generate_reference` engine + 7 prediction helpers |
| `src/.../diligence/project.py` | YAML persistence for projects |
| `tests/test_diligence.py` | 25 tests covering all dimensions |

## Pipeline Status

### Business Architecture (top-down strategic)

| Command | Capability | Status | Validated |
|---------|-----------|--------|-----------|
| `/classify` | `business-classification` | Active | , Ridgeline, EDGE |
| `/decompose-business-model` | `business-model-decomposition` | Active | field-service-recurring, d2c, trade-show |
| `/predict` | `reference-model-prediction` | Active | , Ridgeline, EDGE |
| `/synthesize` | `business-model-synthesis` | Active | , Ridgeline, EDGE |

### Business Architecture → DDD Derivation (structural)

| Command | Capability | Status | Validated |
|---------|-----------|--------|-----------|
| `/derive` | `agentic-ddd-derivation` | Active | Ridgeline (12 BCs), EDGE (9 BCs) |
| `/derive-schema` | `schema-derivation` | Active | Ridgeline, EDGE |
| `/derive-manifests` | `manifest-derivation` | Active | Ridgeline |
| `/derive-analytics` | `analytics-derivation` | Active | EDGE (7 patterns) |
| `/derive-registry` | `registry-derivation` | Active | Ridgeline |
| `/process-analysis` | `process-analysis` | Active | Ridgeline (60 processes, 66 capabilities) |
| `/decompose-vendor` | `vendor-decomposition` | Active | Jobber (20 primitives) |

### Observation + Convergence (bottom-up)

| Command | Capability | Status | Validated |
|---------|-----------|--------|-----------|
| `/observe` | signal collection | Active |  (42 findings) |
| `/diagnose` | `architecture-gap-analysis` | Active |  (8/8 BCs confirmed) |
| Tech stack profiling | detection | Active | 3,931 Wappalyzer signatures |
| Structured extraction | extraction | Active | 3-tier: regex → Ollama → Claude |

### Design Documentation

| Document | What |
|----------|------|
| [DD-0015](https://github.com/semops-ai/semops-orchestrator/blob/main/docs/design-docs/DD-0015-due-diligence-and-osint-pipeline.md) | Pipeline architecture, command specs, derivation knowledge base |
| [TOGAF + BIZBOK Decomposition](research/togaf-bizbok-decomposition.md) | Framework decomposition, pattern/capability alignment |

---

## Capability Guides

| Guide | Coverage | What It Covers |
| --- | --- | --- |
| This document | Full pipeline | Commands, classification, 7 prediction dimensions, engagement flow |
| [CORPUS_COLLECTION.md](CORPUS_COLLECTION.md) | Observe | Crawl, embed, query company-scoped corpora. Observe/diagnose pipeline. |
| [STRUCTURED_EXTRACTION.md](STRUCTURED_EXTRACTION.md) | Observe | Three-tier extraction (regex → Ollama → Claude). Parser registry. |
| [EXTRACTION_VALIDATION.md](EXTRACTION_VALIDATION.md) | Observe | Post-extraction validation checks, guardrails, quality guidance. |
| [3P Data Collection Methodology](research/3p-data-collection-methodology.md) | Observe | OSINT intelligence cycle, source type taxonomy, anti-bot landscape. |
