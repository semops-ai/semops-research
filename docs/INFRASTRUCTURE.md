# Infrastructure

> **Repo:** `semops-research`
> **Owner:** Local ephemeral services + shared infrastructure from semops-data
> **Status:** ACTIVE
> **Version:** 0.2.0
> **Last Updated:** 2026-03-16

---

## Services

> **Port authority:** [PORTS.md](https://github.com/semops-ai/semops-orchestrator/blob/main/docs/PORTS.md) — the single source of truth for all port allocations. Register new ports there before use.

### Owned Services (local ephemeral infrastructure)

| Service | Port | Purpose | Image |
|---------|------|---------|-------|
| Qdrant (local) | 6335 (REST), 6336 (gRPC) | Ephemeral vector collections per company (`ephemeral_*`) | `qdrant/qdrant:latest` |
| Neo4j (local) | 7475 (HTTP), 7688 (Bolt) | Company entity relationship graph | `neo4j:5-community` |

These services are **separate instances** from semops-data infrastructure, running on different ports. They serve ephemeral, engagement-scoped analysis data that does not belong in the shared governance infrastructure.

### Consumed Services (shared from semops-data)

| Service | Port | Purpose |
|---------|------|---------|
| Ollama | 11434 | Embeddings via `nomic-embed-text` (768d vectors) |
| Qdrant (shared) | 6333 | Shared collections: `core_kb`, `published`, `research_*` |
| Docling | 5001 | PDF/document processing |

### Dual-Instance Model

```
semops-data (shared, always-on)          semops-research (local, on-demand)
├── Qdrant :6333                           ├── Qdrant :6335
│   ├── core_kb (permanent)                │   └── ephemeral_* (disposable)
│   ├── published (permanent)              │       ├── ephemeral_
│   └── research_* (project-scoped)        │       ├── ephemeral_
│                                          │       └── ...
├── Neo4j :7474                            ├── Neo4j :7475
│   └── pattern graph, capability registry │   └── company entity graphs
│                                          │
├── Ollama :11434 ◄────────────────────────┤   (shared, stateless)
└── Docling :5001 ◄────────────────────────┘   (shared, stateless)
```

Collection name determines which Qdrant instance is used:
- `ephemeral_*` → local Qdrant (6335)
- Everything else → shared Qdrant (6333)

## Docker Configuration

```bash
# Start local ephemeral infrastructure
docker compose up -d

# Stop (preserve data)
docker compose down

# Stop and destroy ephemeral data
docker compose down -v
```

Services defined in `docker-compose.yml`:
- **research-qdrant** — Qdrant for ephemeral vector collections
- **research-neo4j** — Neo4j with APOC + GDS plugins, no auth (dev mode)

## Environment Variables

> **Convention:** See [GLOBAL_INFRASTRUCTURE.md](https://github.com/semops-ai/semops-orchestrator/blob/main/docs/GLOBAL_INFRASTRUCTURE.md#environment-variable-conventions) for env var standards.

| Variable | Purpose | Required |
|----------|---------|----------|
| `OLLAMA_URL` | Ollama embedding endpoint (default: `http://localhost:11434`) | For RAG pipeline |
| `QDRANT_URL` | Shared Qdrant (default: `http://localhost:6333`) | For core_kb/research queries |
| `QDRANT_LOCAL_URL` | Local Qdrant for ephemeral collections (default: `http://localhost:6335`) | For company dark data |
| `NEO4J_URL` | Local Neo4j Bolt (default: `bolt://localhost:7688`) | For entity graph |
| `NEO4J_HTTP_URL` | Local Neo4j HTTP/browser (default: `http://localhost:7475`) | For graph browser |
| `DOCLING_URL` | Docling PDF processing (default: `http://localhost:5001`) | For PDF sources |
| `ANTHROPIC_API_KEY` | Claude LLM synthesis | For RAG queries |
| `OPENAI_API_KEY` | Fallback LLM provider | Optional |

## Connection Patterns

How this repo connects to infrastructure:

| Service | Instance | Method | Details |
|---------|----------|--------|---------|
| Ollama | shared | `localhost:11434` | Embeddings via `nomic-embed-text` (768d vectors) |
| Qdrant | shared | `localhost:6333` | core_kb, published, research_* collections |
| Qdrant | local | `localhost:6335` | ephemeral_* company collections |
| Neo4j | local | `bolt://localhost:7688` | Company entity graph (Bolt protocol) |
| Neo4j | local | `http://localhost:7475` | Graph browser (HTTP) |
| Docling | shared | `localhost:5001` | PDF/document ingestion |
| Claude API | external | HTTPS | LLM synthesis for RAG queries |

### Module Infrastructure Requirements

| Module | Ollama | Qdrant (shared) | Qdrant (local) | Neo4j (local) | Docling | LLM API |
|--------|--------|-----------------|-----------------|---------------|---------|---------|
| diligence | - | - | - | - | - | - |
| rag.ingest | - | - | - | - | Yes (PDF) | - |
| rag.embed | Yes | Yes | Yes | - | - | - |
| rag.query | - | Yes | Yes | - | - | Yes |

The diligence module has **zero infrastructure dependencies** — it's pure Python with YAML persistence.

## Python Stack

| Property | Value |
|----------|-------|
| **Python version** | `3.10` |
| **Package manager** | `uv` with `pyproject.toml` |
| **Virtual environment** | `.venv/` |
| **Linter/formatter** | `ruff` |
| **Test framework** | `pytest` |

### Key Dependencies

| Library | Purpose | Shared With |
|---------|---------|-------------|
| `pyyaml` | YAML handling (project persistence) | semops, publisher, backoffice, dx-hub, data |
| `requests` | HTTP client (Ollama, Docling APIs) | semops, publisher |
| `qdrant-client` | Vector database client | — |
| `scikit-learn` | Chunk scoring and retrieval | — |
| `crawl4ai` | Web scraping (JS-rendered pages) | — |
| `beautifulsoup4` | HTML parsing fallback | backoffice |
| `anthropic` | Claude LLM synthesis | semops, publisher |
| `openai` | Fallback LLM provider | — |
| `neo4j` | Knowledge graph client (entity extraction → Neo4j) | — |

### Setup

```bash
uv venv && source .venv/bin/activate
uv sync --all-extras

# Start local ephemeral infrastructure
docker compose up -d
```

## Health Checks

```bash
# Shared services (requires semops-data running)
curl http://localhost:11434/api/tags        # Ollama
curl http://localhost:6333/healthz          # Qdrant (shared)
curl http://localhost:5001/health           # Docling

# Local services (requires docker compose up)
curl http://localhost:6335/healthz          # Qdrant (local)
curl http://localhost:7475                  # Neo4j (local)

# Diligence module (no infrastructure needed)
python -c "from research_toolkit.diligence import models; print('OK')"
```

## Consumed By

| Repo | Services Used |
|------|---------------|
| *(none currently)* | — |

## Related Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - This repo's architecture
- [GLOBAL_INFRASTRUCTURE.md](https://github.com/semops-ai/semops-orchestrator/blob/main/docs/GLOBAL_INFRASTRUCTURE.md) - Ecosystem connectivity, network conventions, env var standards
- [PORTS.md](https://github.com/semops-ai/semops-orchestrator/blob/main/docs/PORTS.md) - Port registry (single source of truth)
- [DIAGRAMS.md](https://github.com/semops-ai/semops-orchestrator/blob/main/docs/DIAGRAMS.md) - Infrastructure service diagrams
