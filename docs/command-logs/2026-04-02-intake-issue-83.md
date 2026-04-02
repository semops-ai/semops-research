# Intake Log: Issue  — Discovery agent — lightweight recon for 3P source identification

> **Command:** /intake
> **Date:** 2026-04-02
> **Target:** 
> **Related Session:** [ISSUE-83](../session-notes/ISSUE-83-discovery-agent-recon.md)

## Analysis

### Territory Map

| Entity | Type | Status | Relevance |
|---|---|---|---|
| `osint` | pattern | active | Parent — 5-phase intelligence cycle |
| `semantic-ingestion` | pattern | active | Downstream — chunking + embedding |
| `agentic-rag` | pattern | active | Discovery feeds RAG pipeline |
| `web-signal-collection` (capability) | capability | active → renamed | Was catch-all for collection; renamed to `web-signal-ingestion` |
| `domain-pattern-discovery` | capability | active | Different scope — decomposition outputs, not source discovery |
| `agent-recon` | agent | active | Registered in agents.yaml  |
| `agent-discover` | agent | active | Registered in agents.yaml  |
| ADR-0004 | decision | draft | Two-agent architecture |
| DD-0015 | design doc | active | Pipeline design |

### Delta

- **Extends existing:** `web-signal-ingestion` (formerly `web-signal-collection`) now has upstream producers
- **Fills gap:** No capability existed for source reconnaissance or signal classification
- **Conflicts with:** None
- **Net new:** `web-signal-collection` as a 1P pattern (methodology, not just a capability)

## Result

**Goal:** Build `/recon` and `/discover` for lightweight 3P source identification
**Pattern Matches:** `osint`, `semantic-ingestion` → derived into `web-signal-collection` (1P)
**Capability Matches:** `web-signal-ingestion` (renamed), 2 new capabilities registered
**Recommended Change Type:** Pattern registration + capability registration + capability rename

**Registrations applied:**

| Registry | Change | Repo |
|---|---|---|
| `pattern_v1.yaml` v1.15.0 | Added `web-signal-collection` (1P, derives from osint + semantic-ingestion) | semops-orchestrator |
| `registry.yaml` | Added `web-source-reconnaissance` | semops-data |
| `registry.yaml` | Added `web-signal-classification` | semops-data |
| `registry.yaml` | Renamed `web-signal-collection` → `web-signal-ingestion` | semops-data |
| `agents.yaml` | `/recon` + `/discover` exercise new capabilities | semops-orchestrator |

## Process Manifest

| Field | Value |
| ----- | ----- |
| **Tier** | 1 (Single Issue) |
| **Cognitive Load** | inferential |
| **Bounded Context** | semops-research (acquisition) |
| **Executor** | hybrid |
| **Scale Projection** | scripted |

**Guardrails:**
- Zero-footprint recon must not crawl pages
- Active discovery respects rate limits (3s crawl, 5s external)
- Recon report schema is the handoff contract — must be stable
- Signal patterns are additive (new verticals don't break existing)

## Follow-Up

- Signal pattern catalog migration to YAML (`data/catalogs/signal-patterns/`) — tracked in  acceptance criteria
- Authenticated crawl for login-gated forums — 
