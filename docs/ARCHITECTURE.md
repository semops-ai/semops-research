# Architecture

> **Repo:** `semops-research`
> **Role:** Research/Consulting
> **Status:** ACTIVE
> **Version:** 0.1.0
> **Last Updated:** 2026-03-18
> **Infrastructure:** [INFRASTRUCTURE.md](INFRASTRUCTURE.md)

---

## Role

Corpus meta-analysis, data due diligence, and reference generation — the research & consulting product.

**Key distinction:** This repo owns *research RAG and diligence tooling* with local-first infrastructure (Ollama embeddings). `data-pr` owns *coherence scoring and analytics* with aligned embedding models. `semops-data` owns *infrastructure services*.

## Pipeline Framework: Predict vs Observe, Business vs Technical

The due diligence pipeline operates along two independent axes:

1. **Predict vs Observe** — are we predicting what should exist, or observing what actually exists?
2. **Business vs Technical** — are we looking at business architecture or data/technology architecture?

| | **Predict** (top-down) | **Observe** (bottom-up) |
|---|---|---|
| **Business** | `reference-generation`, `business-model-synthesis`, `agentic-ddd-derivation`, `business-model-decomposition` | `corpus-collection`, `sentiment-extraction` |
| **Technical** | `vendor-decomposition` | `data-due-diligence`, `tech-stack-profiling`, `structured-extraction` |
| **Bridge** | — | `gap-analysis` (TOGAF — compares predicted vs observed across both axes) |

**Predict/Business** answers: "Given a B2B2C trade show in the audio vertical, what business domains, entities, capabilities, and infrastructure would we expect?" Uses BIZBOK, DDD, APQC frameworks.

**Observe/Technical** answers: "From public sources — website, pricing pages, press releases, exhibitor kits, forum threads — what can we actually confirm?" Uses OSINT methodology, web crawling, tech stack detection, structured extraction.

**Gap analysis** bridges both: compare predictions to observations, classify deviations by TOGAF gap categories, produce Findings.

## DDD Classification

> Source: [REPOS.yaml](https://github.com/semops-ai/semops-orchestrator/blob/main/docs/REPOS.yaml)

| Property | Value |
|----------|-------|
| **Layer** | `semops-core` |
| **Context Type** | `core` |
| **Integration Patterns** | `customer-supplier` |
| **Subdomains** | `knowledge-management` |

## Capabilities

> Source: [STRATEGIC_DDD.md](https://github.com/semops-ai/semops-data/blob/main/docs/STRATEGIC_DDD.md) (authoritative capability registry)

| Capability | Quadrant | Status | Description |
|------------|----------|--------|-------------|
| Mirror Architecture Generation | Pipeline | active | Full outside-in pipeline: classify → predict → synthesize → derive. Produces DDD architecture from business inputs alone (DD-0015). 12 slash commands.  |
| Reference Generation | Predict/Business | active | Generate reference models across 7 dimensions from business classification (static + LLM-enriched) |
| Business Model Synthesis | Predict/Business | active | Investment thesis derivation — revenue mechanics, competitive moat, CORE rationale |
| DDD Architecture Derivation | Predict/Business | active | Derive bounded contexts, context map, sagas, agent boundaries from ReferenceModel  |
| Business Model Decomposition | Predict/Business | active | Decomposition of business model archetypes into baseline capability sets. 10 archetype catalogs  |
| Vendor Decomposition | Predict/Technical | active | Decomposition of vendor products into vendor-neutral primitives with explicit enterprise alternatives + data access layer. 21 catalogs  |
| Analytics Pattern Derivation | Predict/Business | active | Derive per-context analytics patterns (metrics, pipelines, feedback loops) from DDD architecture. Attaches to domain patterns, not business models. |
| Agent Training Data Capture | Pipeline | active | Extract structured learnings from engagement reasoning logs into data/agent-training/ for pipeline improvement |
| Data Due Diligence | Observe/Technical | active | Data systems, data model, data management maturity assessment (DAMA-DMBOK, DCAM) |
| Corpus Collection | Observe/Business | active | Company-scoped ephemeral corpus: web crawling, forum pagination, markdown cleaning, dual-instance Qdrant  |
| Tech Stack Profiling | Observe/Technical | active | Self-hosted technology detection using MIT-licensed Wappalyzer signatures. 9 primitives, 3,931 signatures  |
| Structured Extraction | Observe/Technical | active | 3-tier extraction pipeline (regex → Ollama → Claude) with validation guardrails  |
| Sentiment Extraction | Observe/Business | active | Forum sentiment extraction via Ollama/Mistral. Structured: topic, entity, category, sentiment  |
| Synthesis and Simulation | — | in_progress | Scale projection simulations with data lineage tracking (shared with data-pr) |
| Corpus Meta-Analysis | — | active | RAG pipeline: ingest (PDF/web) → embed (Ollama) → query (Claude synthesis) |
| Reference Catalog | — | planned | Unified catalog of reference architectures with semantic search |
| Code Decomposition | Predict/Technical | planned | Decomposition of application source code into classifiable architectural primitives |
| Autonomous Comparative Research | — | planned | End-to-end autonomous research loop with coherence-scored output (shared with semops-orchestrator) |

Every capability must trace to at least one registered pattern (coherence signal). See [pattern_v1.yaml](https://github.com/semops-ai/semops-orchestrator/blob/main/schemas/pattern_v1.yaml).

## Ownership

What this repo owns (source of truth for):

- **Predict side:** Reference generation, business model synthesis, DDD derivation, decomposition catalogs
- **Observe side:** Corpus collection (crawl, clean, embed), structured extraction, sentiment extraction, tech stack profiling
- **Bridge:** Observe/diagnose pipeline (signals → gap analysis → findings)
- 3P framework YAML catalogs (BIZBOK, APQC, DCAM, DAMA) in `data/catalogs/`
- OSINT data collection methodology ([3p-data-collection-methodology.md](research/3p-data-collection-methodology.md))
- Research framework documentation (14+ docs)
- Per-company diligence artifacts (`companies/` — mirror architecture)

What this repo does NOT own (consumed from elsewhere):

- Infrastructure services: Ollama, Qdrant, Docling (semops-data)
- Schema and knowledge model (semops-data)
- Coherence scoring, analytics platform (data-pr)

**Ubiquitous Language conformance:** This repo follows definitions in [UBIQUITOUS_LANGUAGE.md](https://github.com/semops-ai/semops-data/blob/main/schemas/UBIQUITOUS_LANGUAGE.md). Domain terms used in code and docs must match.

## Key Components

### Source Code

```text
src/research_toolkit/
├── config.py                  Shared configuration (Ollama, Qdrant dual-instance, proxy, LLM)
├── rag/                       RAG + collection pipeline
│   ├── ingest.py              Crawl4AI (web) + Docling (PDF) ingestion, forum pagination
│   ├── embed.py               Ollama embeddings → Qdrant storage (dual-instance routing)
│   ├── query.py               Semantic search + LLM synthesis
│   ├── clean.py               Post-crawl markdown denoising (nav, footers, tracking URLs)
│   ├── extract.py             Tier 1 structured extraction (regex parsers)
│   ├── enrich.py              Tier 2 enrichment (Ollama/Mistral classification)
│   ├── extract_sentiment.py   Forum sentiment extraction (Ollama/Mistral)
│   ├── validate.py            Extraction quality guardrails (noise, type mismatch, dupes)
│   ├── graph.py               Entity extraction → Neo4j (typed nodes + relationships)
│   ├── cli.py                 CLI interface (ingest, search, query, extract, enrich, sentiment)
│   └── sources/               Source manifests
└── diligence/                 Data due diligence engine
    ├── models.py              Domain models (Classification, ReferenceModel, Signal, Finding, ...)
    ├── lookups.py             Loads 3P framework data from YAML catalogs (data/catalogs/)
    ├── reference.py           Reference generation engine (domain classification + entity prediction)
    ├── enrichment.py          LLM-augmented vertical enrichment (research, guidance, derivation)
    ├── derivation.py          DDD architecture derivation engine (ReferenceModel → DerivedArchitecture)
    ├── observe.py             Signal collection from company manifests → Signal objects
    ├── diagnose.py            Gap analysis: ReferenceModel vs observed signals → Findings
    ├── project.py             YAML project persistence
    └── signals/               Signal collection modules
        ├── cli.py             CLI (scan, profile)
        └── tech_stack.py      Self-hosted Wappalyzer detection (3,931 signatures)
```

### Domain Model (Diligence Engine)

```text
Classification (partial — can omit vertical, business_model, etc.)
  ├── business_model: [(model, weight), ...]    # Weighted multi-model (G2)
  └── industry / sector / vertical / ...

    ↓ generate_reference(enrich=True)

    1. Research → LLM knowledge + web fetch + RAG corpus
    2. Guidance → static base + LLM refinement
    3. Derive  → fill missing classification fields from evidence
    4. Static  → framework lookups with enriched classification
    5. Enrich  → LLM generates vertical entities + domain contexts
    6. Merge   → static entities + LLM entities, LLM contexts replace static

ReferenceModel
  ├── entities: [PredictedEntity]               # Static + LLM-enriched
  │     └── domain_type: DomainType             # core / supporting / generic (G7)
  ├── domain_contexts: [DomainContext]            # LLM-generated domain partitions (G1+G4)
  │     ├── domain_type: DomainType
  │     ├── entities: [PredictedEntity]
  │     └── aggregate_root: str
  ├── system_mix / processes / capabilities / analytics / team
  ├── metadata: enrichment_provider, classification_derived_fields, urls_fetched
  └── ...

    ↓ derive_architecture(provider=...) — optional LLM enrichment

DerivedArchitecture                            # Issue  — DDD derivation engine
  ├── bounded_contexts: [DerivedBoundedContext] # one per DomainContext
  │     ├── aggregate_root: str                # anchor noun (Rule 1.1)
  │     ├── domain_type: DomainType
  │     ├── pattern_selection: str             # build_custom / buy_adapt / buy_commodity (Rule 4.1)
  │     ├── entities / value_objects / commands / domain_events
  │     ├── upstream_contexts / downstream_contexts / context_map_patterns
  │     └── agent_boundary: AgentBoundary      # 5 agent primitives scoped to context (Rule 6.1)
  ├── context_map: [ContextRelationship]        # directed BC relationships + DDD pattern
  ├── sagas: [Saga]                             # cross-context processes (Step 11)
  ├── coherence_signals: [CoherenceSignal]      # 5 health signals per context (Rule 6.4)
  └── traceability: {field → derivation rule}  # each output traces to BIZBOK source
```

**DomainType** classification is driven by BIZBOK vocabulary layers:

| Source                         | Domain Type | Rationale                        |
| ------------------------------ | ----------- | -------------------------------- |
| BIZBOK Common Reference Model  | SUPPORTING  | Every business has these         |
| Industry Reference Model       | CORE        | What makes this industry different |
| Business model (weight >= 0.5) | CORE        | Primary revenue driver           |
| Business model (weight < 0.5)  | SUPPORTING  | Secondary model                  |
| Product domain                 | CORE        | What the company builds          |
| APQC process-implied           | GENERIC     | Lowest value, commodity          |

### Data Flow (RAG)

```text
Sources (PDF/web)
    → ingest (chunk)
    → embed (Ollama nomic-embed-text → 768d vectors)
    → store (Qdrant)
    → query (semantic search + Claude synthesis)
```

### Scripts

| Script | Capability | Purpose |
| ------ | ---------- | ------- |
| `scripts/bizbok_recon.py` | Reference Generation | BIZBOK viewer recon — login and TOC extraction (Phase 1) |
| `scripts/bizbok_recon2.py` | Reference Generation | BIZBOK viewer recon — DOM inspection (Phase 2) |
| `scripts/bizbok_recon3.py` | Reference Generation | BIZBOK viewer recon — PDF iframe inspection (Phase 3) |
| `scripts/bizbok_recon4.py` | Reference Generation | BIZBOK viewer recon — TOC/bookmarks extraction (Phase 4) |
| `scripts/bizbok_extract_toc.py` | Reference Generation | Extract TOC/outlines from BIZBOK viewer |
| `scripts/bizbok_extract_pages.py` | Reference Generation | Extract Information Map pages from Part 8 Industry Reference Models |
| `scripts/bizbok_extract_all.py` | Reference Generation | Batch-extract full guide text via WebViewer API |
| `scripts/bizbok_parse_entities.py` | Reference Generation | Parse Part 8 extractions into structured entity lists (legacy — data now in YAML catalogs) |
| `scripts/bizbok_compare_entities.py` | Reference Generation | Compare BIZBOK Part 8 concepts against industry catalogs (legacy — data now in YAML) |
| `scripts/_claude.py` | Business Model Synthesis | Run  enrichment via Claude API for quality comparison |
| `scripts/_claude_md.py` | Business Model Synthesis | Generate  enriched reference model markdown via Claude |

### Other Components

| Component | Purpose |
|-----------|---------|
| `docs/research/` | 14+ framework research docs, 3P data collection methodology, decomposition methodology |
| `docs/engagement-logs/` | Per-company reasoning logs from pipeline commands — the intelligence capture layer |
| `companies/` | Per-company engagement artifacts in mirror architecture (domain/outside-in, patterns, infrastructure) |
| `companies/_manifest_schema.json` | Source manifest JSON Schema for corpus collection |
| `data/catalogs/` | YAML catalogs: decompositions (21 vendors), business-models (10 archetypes), processes, verticals |
| `data/agent-training/` | Structured learnings from engagements — training data for pipeline improvement |
| `docker-compose.yml` | Local ephemeral infrastructure: Qdrant (6335) + Neo4j (7475/7688) |
| `docs/USER_GUIDE.md` | Due diligence user guide |
| `tests/` | 173+ tests (diligence, enrichment, observe/diagnose, clean, extraction validation) |

## Dependencies

| Repo | What We Consume |
|------|-----------------|
| semops-data | Ollama (embeddings), Qdrant (vectors), Docling (PDF processing) |

| Repo | What Consumes Us |
|------|------------------|
| *(none yet)* | — |

## Related Documentation

- [GLOBAL_ARCHITECTURE.md](https://github.com/semops-ai/semops-orchestrator/blob/main/docs/GLOBAL_ARCHITECTURE.md) - System landscape
- [DIAGRAMS.md](https://github.com/semops-ai/semops-orchestrator/blob/main/docs/DIAGRAMS.md) - Visual diagrams
- [REPOS.yaml](https://github.com/semops-ai/semops-orchestrator/blob/main/docs/REPOS.yaml) - Structured repo registry
- [INFRASTRUCTURE.md](INFRASTRUCTURE.md) - Services and stack details
- [USER_GUIDE.md](USER_GUIDE.md) - Due diligence user guide
- `docs/research/` - 3P framework research documents

## Provenance

Extracted from [data-pr](https://github.com/semops-ai/data-pr) via .

---

## Versioning Notes

**Status values:**

- `ACTIVE` - Current implemented state (one per doc type)
- `PLANNED-A`, `PLANNED-B`, `PLANNED-C` - Alternative future states

**File naming for planned versions:**

- `ARCHITECTURE.PLANNED-A.md`
- `ARCHITECTURE.PLANNED-B.md`

**When to create a PLANNED version:**

- Significant architectural changes under consideration
- Alternative approaches being evaluated
- Future state design for upcoming work
