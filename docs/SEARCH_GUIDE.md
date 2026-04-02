# Search Guide —  Corpus

> **Collection:** `ephemeral_`
> **Total chunks:** 2,323
> **Sources:** 31 (18  site + 13 forum threads)
> **Last updated:** 2026-03-16

---

## Quick Start

```bash
# Basic search (all sources)
python -m research_toolkit.rag.cli -c ephemeral_ search "turntable"

# RAG query with LLM synthesis
python -m research_toolkit.rag.cli -c ephemeral_ query "What do attendees think about ?"

# Filtered search — forum community only
python -m research_toolkit.rag.cli -c ephemeral_ search "best room" --signal-source customer_voice

# Filtered search — by platform tag
python -m research_toolkit.rag.cli -c ephemeral_ search "tariff pricing" --tags audiogon

# Filtered RAG query — marketing pages only
python -m research_toolkit.rag.cli -c ephemeral_ query "exhibitor booth pricing" --signal-source pricing_page
```

---

## Signal Source Types

Use `--signal-source` to route queries to specific source categories.

| Signal Source | Chunks | What's In It | When to Use |
|---|---:|---|---|
| `customer_voice` | 2,232 | Forum threads — attendee impressions, room rankings, product opinions, complaints | Community sentiment, exhibitor ROI evidence, pain points |
| `marketing` | 29 |  website pages — homepage, about, listening rooms, expo hall, seminars | Official positioning, feature claims, brand voice |
| `industry_research` | 24 | Stereophile and The Absolute Sound show reports | Professional press perspective, product coverage |
| `financial_filings` | 22 | GlobeNewsWire press release ( 2025 results) | Attendance figures, growth metrics, official numbers |
| `pricing_page` | 16 | Exhibit, sponsorship, and ticket pricing pages | Space pricing, ticket tiers, sponsorship inventory |

---

## Tag Reference

Use `--tags` to filter by platform, content type, or topic. Multiple tags (comma-separated) match chunks with ANY of the listed tags.

### Platform Tags

| Tag | Chunks | Forum | Use Case |
|---|---:|---|---|
| `head-fi` | 225 | Head-Fi.org | Headphone/personal audio impressions |
| `stevehoffman` | 305 | Steve Hoffman Music Forums | Music-first perspective, room rankings, vinyl focus |
| `diyaudio` | 900 | diyAudio.com | DIY/engineering perspective, value analysis, active vs. passive debates |
| `asr` | 80 | AudioScienceReview | Measurement-focused, skeptical of subjective claims |
| `wbf` | 510 | What's Best Forum | Ultra-high-end, critical post-show analysis |
| `audiogon` | 35 | Audiogon | Buyer/collector perspective, tariff/pricing anxiety |
| `audioshark` | 100 | AudioShark | Logistics complaints, candid show reports |
| `audiophile-style` | 77 | Audiophile Style | Mixed editorial + community discussion |

### Content Type Tags

| Tag | Chunks | Description |
|---|---:|---|
| `forum` | 2,232 | All forum content (same as `--signal-source customer_voice`) |
| `impressions` | 1,817 | Post-show attendee impressions and product opinions |
| `room-rankings` | 258 | Exhibitor room rankings and best-of lists |
| `show-report` | 101 | Structured show reports (forum + press) |
| `planning` | 100 | Pre-show planning and expectations |
| `critical-analysis` | 433 | Post-show critical reflections (WBF Thoughts & Reflections) |
| `industry-press` | 24 | Professional press coverage |
| `press-release` | 22 | Official company press releases |
| `pricing` | 16 | Pricing pages (exhibitor, sponsorship, tickets) |

### Topic Tags

| Tag | Chunks | Description |
|---|---:|---|
| `headphones` | 114 | Personal audio / ear gear content |
| `measurements` | 80 | Measurement-focused discussion (ASR) |
| `music-first` | 47 | Music/recording quality focus (Steve Hoffman) |
| `value-oriented` | 900 | Value-conscious perspective (diyAudio) |
| `ultra-high-end` | 433 | Cost-no-object systems (WBF) |
| `logistics-complaints` | 100 | Crowding, navigation, venue complaints |
| `attendee-sentiment` | 172 | General attendee opinions and experience |

---

## Example Queries by Use Case

### Exhibitor & Product Research

```bash
# What products were highlighted at the show?
search "best product show" --signal-source customer_voice

# What do attendees think about a specific brand?
search "Magico speakers" --tags forum

# Room rankings — which exhibitors had the best rooms?
search "best room favorite" --tags room-rankings

# Product impressions from measurement-focused community
search "DAC performance" --tags asr
```

### Venue & Logistics

```bash
# Venue complaints and pain points
search "crowding parking navigation" --tags logistics-complaints

# Room acoustics and sound quality issues
search "room acoustics sound bleed" --signal-source customer_voice

# Venue capacity signals
search "too many people crowded" --tags forum
```

### Pricing & Business Model

```bash
# Exhibitor booth pricing
search "booth pricing space cost" --signal-source pricing_page

# Sponsorship inventory and pricing
search "sponsorship price" --signal-source pricing_page

# Ticket pricing and tiers
search "ticket price registration" --signal-source pricing_page

# Tariff impact on industry pricing
search "tariff price increase cost" --tags audiogon
```

### Community Sentiment

```bash
# Overall show experience
search "experience worth attending" --tags impressions

# First-timer vs. repeat attendee perspectives
search "first time tips advice" --tags planning

# Year-over-year comparison
search "better worse than last year" --signal-source customer_voice

# Value perception from budget-conscious community
search "value money worth" --tags value-oriented

# Critical analysis from high-end community
search "disappointed underwhelming" --tags critical-analysis
```

### Industry & Press

```bash
# Official attendance and growth numbers
search "attendance growth record" --signal-source financial_filings

# Professional press show coverage
search "show report highlights" --signal-source industry_research

# Industry trends and market signals
search "industry trend market" --tags forum
```

---

## Combining Filters

Filters are AND-combined: `--signal-source customer_voice --tags head-fi` returns only Head-Fi forum chunks.

Tags are OR-matched: `--tags head-fi,asr` returns chunks from either Head-Fi or ASR.

```bash
# Headphone impressions from Head-Fi only
search "headphone amplifier" --signal-source customer_voice --tags head-fi

# Show reports from both press and community
search "show report best" --tags show-report,impressions

# All forum content except diyAudio (use specific platforms)
search "speaker quality" --tags stevehoffman,wbf,head-fi,asr
```

---

## Data Pipeline

```
Sources (manifest) → Crawl4AI → Clean → Chunk → Embed (Ollama) → Qdrant
                                    ↓
                              Sentiment Extract (Ollama) → Neo4j
```

- **Manifest:** [companies//mirror/domain/sources.json](../companies//mirror/domain/sources.json) — 29 sources with signal_source, tags, max_pages
- **Sentiment data:** [companies//mirror/staging/sentiment-extraction.json](../companies//mirror/staging/sentiment-extraction.json) — 202 deduplicated records
- **Sentiment summary:** [companies//sentiment-summary.md](../companies//sentiment-summary.md)
- **Forum research:** [companies//mirror/domain/forum-crawl-research.md](../companies//mirror/domain/forum-crawl-research.md)

## Related

- [CORPUS_COLLECTION.md](CORPUS_COLLECTION.md) — Corpus collection methodology
- [USER_GUIDE.md](USER_GUIDE.md) — Data due diligence reference generation
- [ARCHITECTURE.md](ARCHITECTURE.md) — Repo architecture and ownership
