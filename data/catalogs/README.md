# Data Catalogs

Structured reference data that the pipeline consumes. Each catalog follows the grow-through-engagement pattern: if a match exists, use it directly (static lookup); if no match exists, the schema + nearest-neighbor examples become prompt context for LLM reasoning, and the output is saved as a new catalog entry.

Every catalog directory has a `_schema.yaml` documenting the entry format.

## Catalog Directory

| Directory | Keyed By | What It Answers | Pipeline Consumer |
|-----------|----------|-----------------|-------------------|
| [analytics/](analytics/) | Three axes (see below) | What metrics, benchmarks, and measurement patterns apply? | `/predict`, `/derive-analytics` |
| [brand-archetypes/](brand-archetypes/) | business model + vertical | What voice, messaging, and proof patterns define this archetype? | `/classify` |
| [business-models/](business-models/) | revenue model | What capabilities does this type of business need? | `/predict`, `/decompose-business-model` |
| [categories/](categories/) | architectural category | What universal primitives define this category (CRM, PIM, DAM…)? | `/decompose-vendor` |
| [decompositions/](decompositions/) | vendor product | What neutral primitives does this product provide? | `/predict`, `/decompose-vendor` |
| [frameworks/](frameworks/) | framework name | What does this 3P framework define (DAMA, DCAM)? | `/predict` |
| [industries/](industries/) | BIZBOK industry | What entities, capabilities, and value streams exist in this industry? | `/predict`, `/classify` |
| [messaging-analysis/](messaging-analysis/) | company | How does a company present itself publicly? | `/classify` (Stage 1b) |
| [operational/](operational/) | scale / business type | What operational expectations apply at this scale? | `/predict` (via `lookups.py`) |
| [processes/](processes/) | bounded context | What process sets apply to this context? | `/derive` |
| [product-domains/](product-domains/) | product domain | What entities does this product domain add? | `/predict` |
| [verticals/](verticals/) | vertical | What product language, content types, and customer segments define this vertical? | `/classify` |

## Analytics Catalogs (Three Orthogonal Axes)

The `analytics/` directory has three subdirectories representing independent measurement axes. A company's full analytics profile is the union of all three:

| Subdirectory | Keyed By | Measures | Example |
|-------------|----------|----------|---------|
| `business-model/` | revenue model (SaaS, marketplace…) | Financial health — same metrics regardless of vertical | SaaS → MRR, churn, LTV:CAC |
| `domain/` | archetype (field-service, event-management…) | Operational excellence — derived from bounded contexts | field-service → route-efficiency, job-quality-score |
| `surface/` | surface type (web, mobile, digital-signage…) | Instrumentable tech stack — what's measurable given the surface | web → bounce rate, session duration, conversion |

Plus `scale-expectations.yaml` at the analytics root — functional analytics maturity by revenue range (bi, product, marketing, customer × table_stakes/mature/red_flag).

## Relationship to Code

Catalogs are consumed two ways:

1. **By agent commands** (prompt-level) — `/predict`, `/derive-analytics`, `/classify`, etc. read YAML catalogs directly as context
2. **By Python code** — `src/research_toolkit/diligence/lookups.py` loads all domain data from YAML at import time:

| Catalog Directory  | Python Variables                                                                                |
| ------------------ | ----------------------------------------------------------------------------------------------- |
| `industries/`      | `UNIVERSAL_ENTITIES`, `ENTITIES_BY_INDUSTRY`, `DOMAIN_CONTEXTS_BY_INDUSTRY`                     |
| `business-models/` | `ENTITIES_BY_BUSINESS_MODEL`                                                                    |
| `product-domains/` | `ENTITIES_BY_PRODUCT_DOMAIN`                                                                    |
| `processes/`       | `APQC_CATEGORIES`, `PROCESS_SCALE_EXPECTATIONS`                                                 |
| `frameworks/`      | `DCAM_COMPONENTS`, `DCAM_SCALE_EXPECTATIONS`, `DAMA_KNOWLEDGE_AREAS`, `DAMA_SCALE_EXPECTATIONS` |
| `operational/`     | `SYSTEM_MIX`, `NEUTRAL_CAPABILITIES`, `NEUTRAL_CAPABILITY_BY_SCALE`, `TEAM_BY_SCALE`            |
| `analytics/`       | `ANALYTICS_BY_SCALE`                                                                            |

Revenue range normalization maps remain in Python (they are logic, not data).

## Conceptual Model

```
Classification (inputs)
    │
    ├── business-models/     → Required CAPABILITIES (Architecture Building Blocks)
    ├── decompositions/      → Vendor PRIMITIVES (Solution Building Blocks)
    ├── industries/          → ENTITIES and value streams (BIZBOK)
    ├── analytics/           → Required METRICS and benchmarks
    │   ├── business-model/  →   ...by revenue model
    │   ├── domain/          →   ...by operational archetype
    │   ├── surface/         →   ...by tech surface
    │   └── scale-expectations.yaml → ...by revenue scale
    └── operational/         → Scale-dependent operational expectations
```
