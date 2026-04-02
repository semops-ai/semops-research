# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Role in Global Architecture

**Bounded Context:** Research & Consulting Product

```text
semops-orchestrator [PLATFORM/DX]
        |
        └── semops-data [ORCHESTRATOR]
                |
                └── semops-research [RESEARCH/CONSULTING] <-- YOU ARE HERE
                    |
                    ├── Owns: Research product & consulting methodology
                    |   - RAPTOR RAG pipeline (ingest/embed/query/synthesize)
                    |   - Data due diligence product (classify/predict/observe/diagnose)
                    |   - 3P framework research docs (BIZBOK, TOGAF, DCAM, APQC, DAMA)
                    |   - Reference generation engine
                    |
                    └── Uses: Infrastructure from semops-data
                        - Ollama (port 11434) — local embeddings
                        - Qdrant (port 6333) — vector storage
                        - Docling (port 5001) — document processing
```

**Key Ownership Boundary:**

- This repo owns **research products** — RAG pipelines, due diligence methodology, framework research
- `semops-data` owns **infrastructure** — Qdrant, Docling, Ollama, PostgreSQL
- `data-pr` owns **data engineering** — coherence scoring, synthetic data, profiling, analytics

**Extracted from:** `data-pr` (see )

**Global Docs Location:** `

## Tech Stack

- **Python 3.10+** with pyproject.toml packaging
- **Ollama** for embeddings (nomic-embed-text, local, free)
- **Qdrant** for vector storage
- **Docling** for PDF/document processing
- **Crawl4AI/Playwright** for web scraping
- **Claude API** for LLM synthesis (sparingly)
- **Pure Python** diligence module (no infra dependencies)

## Common Commands

```bash
# Setup
uv venv && source .venv/bin/activate
uv sync --all-extras

# Linting
ruff check . && ruff format .

# Testing
pytest                              # All tests (diligence: no infra needed)
pytest tests/test_diligence.py      # Run single test file
pytest tests/test_diligence.py::TestGenerateReference::test_generates_reference  # Single test
pytest -m "not integration"         # Skip integration tests

# RAG Pipeline
python -m research_toolkit.rag.cli status
python -m research_toolkit.rag.cli ingest --type pdf
python -m research_toolkit.rag.cli query "What causes AI transformation to fail?"
```

## Mirror Architecture Generation Pipeline (DD-0015)

Agent-native commands for outside-in engagement — classify a company, build the architecture, produce mirror artifacts. Design: [DD-0015](https://github.com/semops-ai/semops-orchestrator/blob/main/docs/design-docs/DD-0015-due-diligence-and-osint-pipeline.md).

| Command | What It Does |
|---------|-------------|
| `/classify` | Business classification from company inputs → classification.yaml |
| `/decompose-business-model` | Build archetype catalog when none exists → data/catalogs/business-models/ |
| `/predict` | Generate reference model from catalogs + frameworks → reference-model.yaml |
| `/synthesize` | Investment thesis, domain typing, cross-domain patterns → business-model.yaml |
| `/derive` | Mechanical DDD architecture → STRATEGIC_DDD.md + UBIQUITOUS_LANGUAGE.md |
| `/derive-analytics` | Per-context analytics patterns → mirror/domain/patterns/analytics/ |
| `/derive-schema` | PostgreSQL schema per bounded context |
| `/derive-registry` | Per-engagement pattern + capability registry |
| `/derive-manifests` | Bronze/silver/gold/governance layer manifests |
| `/decompose-vendor` | Vendor product → neutral primitives with explicit enterprise alternatives |
| `/agent-training` | Extract structured learnings from engagement logs → data/agent-training/ |

**Engagement artifacts:** `companies/{name}/mirror/` (client-facing outputs)
**Reasoning logs:** `docs/engagement-logs/{name}/` (pipeline intelligence, stays in semops-research)
**Agent training:** `data/agent-training/` (structured learnings for pipeline improvement)

## Code Architecture

### Diligence Engine

Two-path reference generation from `Classification` → `ReferenceModel`:

```text
Classification (partial inputs)
    │
    ├─[enrich=False]─→ Static lookups only (15 lookup tables)
    │                   └── 7 dimensions: system_mix, entities, processes,
    │                       capabilities, analytics, neutral_capabilities, team
    │
    └─[enrich=True]──→ LLM enrichment pipeline:
                        1. Research (LLM knowledge + web fetch + RAG)
                        2. Guidance (static base + LLM refinement)
                        3. Derive (fill missing classification fields)
                        4. Static (framework lookups with enriched classification)
                        5. Enrich (LLM generates vertical entities + domain contexts)
                        6. Merge (static entities + LLM entities, LLM contexts replace static)
```

**Domain type assignment** (DDD strategic classification):

- `CORE` — Industry reference model, business model (weight ≥ 0.5), product domain
- `SUPPORTING` — BIZBOK Common Reference Model, business model (weight < 0.5)
- `GENERIC` — APQC process-implied entities

### RAG Pipeline

```text
Sources (PDF/web) → ingest (chunk) → embed (Ollama) → store (Qdrant) → query (Claude)
```

CLI: `python -m research_toolkit.rag.cli [status|ingest|query|search|sources|cleanup]`

## Session Notes

Document work sessions tied to GitHub Issues in `docs/session-notes/`:

- **Format:** `ISSUE-NN-description.md` (one file per issue, append-forever)
- **Structure:** Date sections within file for chronological tracking
- **Index:** Update `docs/SESSION_NOTES.md` with new entries

## Key Files

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Repo architecture and ownership
- [docs/INFRASTRUCTURE.md](docs/INFRASTRUCTURE.md) - Infrastructure dependencies
- [docs/USER_GUIDE.md](docs/USER_GUIDE.md) - Data due diligence: reference generation (classify → predict)
- [docs/CORPUS_COLLECTION.md](docs/CORPUS_COLLECTION.md) - Corpus collection: crawl → embed → query → entity extraction
- [docs/STRUCTURED_EXTRACTION.md](docs/STRUCTURED_EXTRACTION.md) - Structured extraction: regex → Ollama → Claude → Neo4j
- [docs/EXTRACTION_VALIDATION.md](docs/EXTRACTION_VALIDATION.md) - Post-extraction validation checks and guardrails
- [docs/decisions/](docs/decisions/) - Architecture Decision Records
- [docs/session-notes/](docs/session-notes/) - Session logs by issue
- [docs/research/](docs/research/) - 3P framework research documents
- [~/.claude/CLAUDE.md](~/.claude/CLAUDE.md) - Global instructions (user-level)
