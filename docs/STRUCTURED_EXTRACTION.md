# Structured Extraction — User Guide

Extract structured, queryable data from company web pages and documents. Turns marketing pages, pricing tables, and directories into typed Neo4j graph nodes — without relying on LLM interpretation of raw text.

## When to Use This

After you've classified a company and generated a reference model ([USER_GUIDE.md](USER_GUIDE.md) stages 1–2), you need to **observe** what actually exists. The corpus collection pipeline ([CORPUS_COLLECTION.md](CORPUS_COLLECTION.md)) crawls and embeds pages for semantic search. The structured extraction pipeline goes further — it parses specific page types into typed records you can query, count, and compare against predictions.

Use structured extraction when the source page has **repeating structure** — exhibitor directories, pricing tables, sponsorship inventories, ticket types. Don't use it for prose content (press releases, forum threads, show reports) — those go through the LLM extraction path in `graph.py` (see [CORPUS_COLLECTION.md](CORPUS_COLLECTION.md)).

## Three-Tier Architecture

Each tier handles what the previous tier can't:

```text
Tier 1: Regex                    Tier 2: Ollama              Tier 3: Claude
─────────────────                ──────────────              ──────────────
Deterministic facts from         Classification that         Cross-source reasoning,
structured markup.               requires domain             gap analysis, synthesis.
                                 knowledge.
Free. Instant.                   Free. ~2 min/500 items.     ~$0.02 per synthesis call.

Examples:                        Examples:                   Examples:
• Brand names + locations        • Brand → product category  • Reference model validation
• Sponsorship items + prices     • Location code → type      • Revenue intelligence
• Ticket types + pricing         • Sponsorship → visibility  • Exhibitor concentration
• SOLD/available status            type classification       • Updated gap assessment
```

## Quick Start

```bash
# 1. Run structured extraction (Tier 1 — regex)
python -m research_toolkit.rag.cli extract companies/acme

# 2. Enrich with Ollama classification (Tier 2)
python -m research_toolkit.rag.cli enrich companies/acme

# 3. Enrich and write to Neo4j graph
python -m research_toolkit.rag.cli enrich companies/acme \
    --graph --clear \
    --company "Acme Corp" --event "Acme Expo 2026"
```

## Setting Up a New Company

### 1. Create the company directory and manifest

```text
companies/
└── acme/
    └── sources.json      ← company source manifest
```

The manifest follows `companies/_manifest_schema.json`. For sources with structured content, add the `extract_type` field to route to the right parser:

```json
{
  "company": "Acme Corp",
  "collection": "ephemeral_acme",
  "website": "https://acme-expo.com",
  "sources": [
    {
      "url": "https://acme-expo.com/exhibitors/",
      "title": "Acme Exhibitor Directory",
      "source_type": "web",
      "signal_source": "marketing",
      "tags": ["exhibitor-directory", "js-rendered"],
      "extract_type": "exhibitor-directory"
    },
    {
      "url": "https://acme-expo.com/sponsors/",
      "title": "Acme Sponsorship Packages",
      "source_type": "web",
      "signal_source": "pricing_page",
      "tags": ["sponsorship", "pricing"],
      "extract_type": "sponsorship-inventory"
    },
    {
      "url": "https://acme-expo.com/tickets/",
      "title": "Acme Tickets",
      "source_type": "web",
      "signal_source": "pricing_page",
      "tags": ["tickets", "pricing"],
      "extract_type": "ticket-pricing"
    },
    {
      "url": "https://acme-expo.com/about/",
      "title": "Acme About Page",
      "source_type": "web",
      "signal_source": "marketing",
      "tags": ["about", "marketing"]
    }
  ]
}
```

Sources **without** `extract_type` are skipped by the extraction pipeline — they're for the ephemeral corpus (semantic search) or LLM entity extraction.

### 2. Available extract types

| `extract_type` | Parser | What it extracts |
| --- | --- | --- |
| `exhibitor-directory` | `parse_exhibitor_brands` | Brand names, exhibitor companies, locations, URLs |
| `sponsorship-inventory` | `parse_sponsorship_items` | Item names, categories, pricing, SOLD/available status |
| `ticket-pricing` | `parse_ticket_types` | Ticket names, regular/onsite pricing, inclusions |
| `exhibitor-spaces` | `parse_exhibitor_spaces` | Space types and pricing |

### 3. Tags that affect crawling

| Tag | Effect |
| --- | --- |
| `js-rendered` | Crawl4AI waits for `networkidle` before scraping (required for pages that load content via JavaScript) |

### 4. Run extraction

```bash
python -m research_toolkit.rag.cli extract companies/acme
```

This reads `sources.json`, finds sources with `extract_type`, crawls each one (if not already cached), and runs the appropriate parser. Crawled markdown is cached as `<extract_type>-raw.md` in the company directory.

Output is saved to `companies/acme/structured-extraction.json`.

### 5. Enrich with Ollama (Tier 2)

```bash
python -m research_toolkit.rag.cli enrich companies/acme
```

Reads `structured-extraction.json` and:

- Classifies exhibitor brands into product categories via Ollama/Mistral (batches of 50)
- Classifies locations by type (Expo Hall, Listening Room, etc.) via regex
- Adds visibility type to sponsorship items
- Calculates minimum sold sponsorship revenue

Output saved to `companies/acme/enriched-extraction.json`.

### 6. Write to Neo4j (optional)

```bash
python -m research_toolkit.rag.cli enrich companies/acme \
    --graph --clear \
    --company "Acme Corp" --event "Acme Expo 2026"
```

Creates typed graph nodes and relationships:

| Node Type | Example |
| --- | --- |
| `Event` | The show/event |
| `Brand` | Manufacturer brands (with `product_category`) |
| `Exhibitor` | Companies exhibiting (with URL) |
| `SponsorshipItem` | Sponsorship inventory (with `price`, `sold`, `category`) |
| `TicketType` | Ticket types (with `regular_price`, `onsite_price`, `inclusions`) |

| Relationship | Meaning |
| --- | --- |
| `Brand -[:EXHIBITED_AT]-> Event` | Brand shown at event |
| `Exhibitor -[:CARRIES]-> Brand` | Exhibitor carries brand |
| `Exhibitor -[:LOCATED_AT]-> Event` | With `location` and `location_type` properties |
| `SponsorshipItem -[:SPONSORS]-> Event` | Sponsorship for event |
| `Event -[:OFFERS_TICKET]-> TicketType` | Event sells ticket type |

## Adding a New Parser

When you encounter a new structured page type:

1. **Write the parser** in `src/research_toolkit/rag/extract.py` — a function that takes markdown and returns a list of dataclasses
2. **Write a serializer** — converts the dataclass list to a JSON-compatible dict
3. **Register it** in `PARSER_REGISTRY`:

```python
PARSER_REGISTRY["new-page-type"] = (
    parse_new_page_type,     # parser function
    _serialize_new_type,     # serializer function
    "new_page_type",         # result key in output dict
)
```

4. **Add to schema** — add the new `extract_type` value to `companies/_manifest_schema.json`
5. **Tag sources** — add `"extract_type": "new-page-type"` to the relevant source in `sources.json`

The parsers are page-structure-specific — a sponsorship parser built for 's markdown structure may need adjustment for a different trade show's layout. The registry pattern means you can have multiple parsers for the same concept (e.g., `sponsorship-inventory-v2`) without breaking existing ones.

## Tier 3: Claude Synthesis

Tier 3 is not automated — it's a one-shot analysis script that you run after Tiers 1–2 are complete. See `scripts/tier3_synthesis.py` for the pattern.

The Claude call takes structured extraction output + the reference model and produces:

- Reference model entity validation (which predictions now have evidence?)
- Revenue intelligence (sponsorship revenue, space distribution, ticket model)
- Cross-source findings (exhibitor concentration, category-location correlation)
- Updated gap assessment

Cost is typically $0.01–0.03 per synthesis call.

## Extraction Validation

Post-extraction validation runs automatically for LLM-based entity extraction (`build_company_graph`) but applies conceptually to all tiers. See [EXTRACTION_VALIDATION.md](EXTRACTION_VALIDATION.md) for the full validation guide.

| Tier | Validation Value |
| --- | --- |
| Regex (structured pages) | Low — regex output is deterministic, but page layout changes could introduce garbage |
| Ollama (classification) | Medium — misclassification is the main risk |
| Claude (reasoning) | High — unstructured sources produce the most noise, validation is most valuable here |

## Example:  Results

The  trade show was the first test case. Results from the full pipeline:

| Extraction | Count | Notes |
| --- | --- | --- |
| Exhibitor brands | 588 | 309 unique exhibitors, 15 product categories |
| Sponsorship items | 51 | 24 sold, 27 available, $105K+ min sold revenue |
| Ticket types | 6 | $0–$150 range, Gold Pass (10 perks), Trade Pass (5 perks) |
| Neo4j graph | 955 nodes | 1,937 relationships |

Key findings:

- Top 5 exhibitors carry 27% of all brands (hub-and-spoke distribution)
- Sponsorship sell-through: 47% (physical signage sells best)
- Reference model validation upgraded from 15/21 to 17/21 CORE entities confirmed

See `companies//` for the full output.

## Source Files

| File | What |
| ---- | ---- |
| `src/.../rag/extract.py` | Tier 1 regex parsers + parser registry + manifest-driven extraction |
| `src/.../rag/enrich.py` | Tier 2 Ollama classification (brand categories, location types) |
| `src/.../rag/graph.py` | `write_structured_extraction` — Neo4j graph writer |
| `src/.../rag/cli.py` | `extract` and `enrich` CLI subcommands |
| `companies/_manifest_schema.json` | JSON Schema for source manifests (includes `extract_type`) |
| `tests/test_extract.py` | 24 parser tests with fixture data |
| `tests/test_enrich.py` | 11 enrichment tests |
