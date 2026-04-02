# Intake Log: Issue  — Company-scoped ephemeral corpus collection (dark data capture)

> **Command:** /intake
> **Date:** 2026-03-16
> **Target:** 

## Analysis

### Territory Map

**Entity References Found:**
- `corpus-meta-analysis` (capability, active) — direct match, owns the RAG pipeline being extended
- `semantic-ingestion` (pattern, active) — ingestion pipeline where byproducts are first-class
- `raptor` (pattern, active) — research synthesis on corpus (downstream consumer)
- `agentic-rag` (pattern, active) — query interface for ephemeral collections
- `data-due-diligence` (capability, active) — consumer via `enrichment.py._search_corpus`
- PROJECT-24 (project spec, draft) — direct parent, Steps 1-2 are this work
- ADR-0005 (decision, in progress) — authority for corpus taxonomy
-  (issue, open) — observe/diagnose pipeline, overlapping signal collection scope

**Capability → Pattern Coverage:**

| Capability | Patterns | Gap? |
|-----------|----------|------|
| `corpus-meta-analysis` | `semantic-ingestion`, `raptor`, `agentic-rag` | No |
| `data-due-diligence` | `ddd`, `data-modeling`, `mirror-architecture`, etc. | Minor — `source-classification` not registered |

**Existing Coverage:**
- Ingest pipeline (Crawl4AI + Docling + Qdrant + Ollama) — all working, single-collection
- Company web fetching in `enrichment.py._fetch_company_pages` — ephemeral in-memory, not persisted
- Source manifest format (`manifest.json`) — exists but global only
- ADR-0005 defines corpus tiers; PROJECT-24 defines execution plan

### Delta

- **Extends existing:** Multi-collection support for working RAG pipeline
- **Fills gap:** Bridge between ephemeral web fetch (discarded) and persistent corpus (Qdrant)
- **Fills gap:** No local infrastructure in semops-research for engagement-scoped analysis
- **Net new:** Dual-instance model (shared core_kb + local ephemeral), Neo4j entity graph for company content, company-scoped source manifests
- **Conflicts:** None

### Architecture Decision (during evaluation)

Local ephemeral infrastructure in semops-research rather than shared semops-data:
- Ephemeral = disposable, doesn't belong in governance infra
- Need both running simultaneously (core_kb queries + ephemeral analysis)
- Aligns with mirror architecture (company analysis is isolated)
- Consulting model: spin up per-engagement, tear down when done
- Client repo extraction: local infra travels with the analysis when peeling off a client repo (e.g., -pr)

Ports: Qdrant 6335, Neo4j 7475/7688 (avoids semops-data conflicts)

## Result

**Goal:** Multi-collection ephemeral corpus with local infrastructure for company dark data capture
**Pattern Matches:** `semantic-ingestion`, `raptor`, `agentic-rag`
**Capability Matches:** `corpus-meta-analysis` (direct), `data-due-diligence` (consumer)
**Recommended Change Type:** Extension of existing capability
**Delta Summary:** Extends `corpus-meta-analysis` with multi-collection support and local Qdrant + Neo4j for ephemeral company analysis. Dual-instance model enables querying shared core_kb and local ephemeral_* simultaneously.

## Follow-Up

- Link as child of PROJECT-24 (Steps 1-2)
- Consider  relationship —  provides infrastructure  needs
- Register `source-classification` pattern (minor governance gap, )
- Update INFRASTRUCTURE.md when docker-compose is created
- Register ports in semops-orchestrator PORTS.md
