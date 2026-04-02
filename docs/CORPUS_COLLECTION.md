# Corpus Collection — User Guide

Crawl, embed, and query company-scoped dark data for due diligence signal collection. Build ephemeral corpora from public web pages, PDFs, and press releases.

## When to Use This

After classifying a company and generating a reference model ([USER_GUIDE.md](USER_GUIDE.md)), you need observable signals to compare against predictions. This pipeline:

1. **Crawls** company web pages and PDFs (Crawl4AI + Docling)
2. **Cleans** the markdown (strips navigation, footers, tracking URLs)
3. **Chunks** the text with sliding window overlap
4. **Embeds** chunks via Ollama (nomic-embed-text)
5. **Stores** in a company-scoped Qdrant collection (`ephemeral_<company>`)

You can then search the corpus semantically, extract entities into a Neo4j knowledge graph, or run the structured extraction pipeline ([STRUCTURED_EXTRACTION.md](STRUCTURED_EXTRACTION.md)) on specific page types.

## Quick Start

```bash
# 1. Create company manifest
# See companies//sources.json for a complete example

# 2. Ingest all sources into ephemeral collection
python -m research_toolkit.rag.cli ingest \
    -m companies/acme/sources.json

# 3. Check status
python -m research_toolkit.rag.cli -c ephemeral_acme status

# 4. Search the corpus
python -m research_toolkit.rag.cli -c ephemeral_acme search "sponsorship pricing"

# 5. RAG query with LLM synthesis
python -m research_toolkit.rag.cli -c ephemeral_acme query "What are the exhibitor space types and pricing?"
```

## Company Source Manifest

Each company has a `sources.json` manifest in `companies/<name>/`. The schema is defined in `companies/_manifest_schema.json`.

```json
{
  "company": "Acme Corp",
  "collection": "ephemeral_acme",
  "website": "https://acme.com",
  "sources": [
    {
      "url": "https://acme.com/about/",
      "title": "Acme About Page",
      "source_type": "web",
      "signal_source": "marketing",
      "tags": ["about", "positioning"],
      "reliability": 0.5
    },
    {
      "url": "https://acme.com/pricing/",
      "title": "Acme Pricing Page",
      "source_type": "web",
      "signal_source": "pricing_page",
      "tags": ["pricing"],
      "reliability": 0.9
    }
  ]
}
```

### Source Fields

| Field | Required | Description |
| --- | --- | --- |
| `url` | Yes | URL to fetch |
| `title` | Yes | Human-readable title |
| `source_type` | Yes | `"web"` (Crawl4AI) or `"pdf"` (Docling) |
| `signal_source` | Yes | SignalSource enum — categorizes the source for observe/diagnose |
| `tags` | No | Freeform tags for filtering. `"js-rendered"` triggers networkidle wait. |
| `reliability` | No | Expected reliability 0–1 (default 0.5) |
| `notes` | No | Collection notes — what to expect, known issues |
| `extract_type` | No | Routes to structured extraction parser (see [STRUCTURED_EXTRACTION.md](STRUCTURED_EXTRACTION.md)) |

### Signal Source Types

| Type | Category | Examples |
| --- | --- | --- |
| `marketing` | Non-tech | Homepage, about page, brochures |
| `pricing_page` | Non-tech | Pricing, sponsorship, ticket pages |
| `financial_filings` | Non-tech | Press releases, annual reports |
| `customer_voice` | Non-tech | Forum threads, reviews, testimonials |
| `industry_research` | Non-tech | Trade publication coverage |
| `job_postings` | Both | LinkedIn, careers page |
| `api_docs` | Tech | API documentation |
| `tech_stack` | Tech | Technology pages, stack disclosures |
| `open_source` | Tech | GitHub repos |

## Observe / Diagnose Pipeline

After ingesting sources, run the observe/diagnose pipeline to collect signals and compare against reference model predictions.

```python
from research_toolkit.diligence.observe import observe, observe_status
from research_toolkit.diligence.diagnose import diagnose

# Collect signals from manifest
signals = observe("companies/acme/sources.json", ingest=False)

# Check corpus health
observe_status("ephemeral_acme")

# Compare signals against reference model predictions
findings = diagnose(signals, reference_model)
```

## Knowledge Graph Extraction

For unstructured content (prose, press releases, forum threads), use LLM-based entity extraction to build a Neo4j knowledge graph:

```python
from research_toolkit.rag.graph import build_company_graph

# Extract entities from corpus → validate → write to Neo4j
result = build_company_graph(
    collection="ephemeral_acme",
    company="Acme Corp",
    max_chunks=30,
    domain_keywords=["audio", "speaker", "amplifier"],
)

print(f"Nodes: {result['nodes']}, Relationships: {result['relationships']}")
print(f"Error rate: {result['error_rate']:.0%}")
```

This automatically runs the validation pipeline (see [EXTRACTION_VALIDATION.md](EXTRACTION_VALIDATION.md)) and excludes noise entities before writing.

For structured content (directories, pricing tables), use the structured extraction pipeline instead — see [STRUCTURED_EXTRACTION.md](STRUCTURED_EXTRACTION.md).

## Infrastructure

The corpus collection pipeline uses ephemeral infrastructure separate from the shared research corpus:

| Service | Port | Purpose |
| --- | --- | --- |
| Qdrant (ephemeral) | 6335 | Company-scoped vector collections |
| Qdrant (shared) | 6333 | Core research corpus |
| Neo4j | 7688 (Bolt) / 7475 (HTTP) | Entity relationship graphs |
| Ollama | 11434 | Embeddings (nomic-embed-text) + entity extraction (Mistral) |
| Docling | 5001 | PDF processing |

Collections starting with `ephemeral_` are automatically routed to the local Qdrant instance (6335). All other collections use the shared instance (6333).

```bash
# Start ephemeral infrastructure
cd /path/to/semops-research
docker compose up -d
```

## Markdown Cleaning

Post-crawl cleaning (`clean.py`) removes website chrome before chunking:

- Navigation menus and footer links
- Cookie consent banners
- Tracking URLs and UTM parameters
- Inline images (preserves alt text)
- Social media link bars

The cleaner is intentionally conservative — it removes structural noise but preserves all prose, headings, bold text, and data (prices, product names, etc.).

## Source Files

| File | What |
| ---- | ---- |
| `src/.../rag/ingest.py` | Crawl (Crawl4AI/Docling) + chunk pipeline |
| `src/.../rag/embed.py` | Ollama embeddings → Qdrant storage |
| `src/.../rag/query.py` | Search, RAG synthesis, source listing |
| `src/.../rag/clean.py` | Post-crawl markdown denoising |
| `src/.../rag/graph.py` | LLM entity extraction → Neo4j |
| `src/.../rag/cli.py` | CLI commands (ingest, search, query, status, sources) |
| `src/.../diligence/observe.py` | Signal collection from manifests |
| `src/.../diligence/diagnose.py` | Gap analysis (predicted vs observed) |
| `src/.../config.py` | Dual-instance Qdrant routing |
| `companies/_manifest_schema.json` | Manifest JSON Schema |
| `tests/test_clean.py` | Markdown cleaning tests |
| `tests/test_observe_diagnose.py` | Observe/diagnose pipeline tests |
