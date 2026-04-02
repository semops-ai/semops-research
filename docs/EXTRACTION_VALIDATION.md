# Extraction Validation — User Guide

Post-extraction validation for entity extraction results. Catches noise, type mismatches, and duplicates before data enters Neo4j.

## Overview

Validation runs automatically inside `build_company_graph` after LLM entity extraction and before Neo4j write. It uses heuristic checks (no LLM cost) to flag quality issues. The pipeline is tier-agnostic — it validates output regardless of which extraction method produced it.

## Checks

| Check | What It Catches | Severity | False Positive Risk |
| --- | --- | --- | --- |
| `check_noise_entities` | Entities with noise-domain keywords (quantum, crypto, pharma, etc.) | error | Low — keyword list is conservative |
| `check_type_mismatches` | Person name typed as Company, corporate suffix typed as Person, generic words as entities | warning | Medium — eponymous brands trigger false positives |
| `check_duplicates` | Case variants of same entity ( vs ) | warning | Low — exact normalized match required |
| `check_source_relevance` | Sources whose entities share zero overlap with other sources | warning | Medium — legitimate niche sources may have unique entities |

## Guardrail

| Error Rate | Action |
| --- | --- |
| < 20% | Auto-exclude error-severity entities, keep warnings, write to Neo4j |
| 20–50% | Halt Neo4j write, return report for agent/human review |
| > 50% | Halt — extraction is fundamentally broken |

## Usage

Validation is integrated into `build_company_graph` and runs automatically. You can also call it directly:

```python
from research_toolkit.rag.validate import validate_extractions, filter_extractions

# Run validation
report = validate_extractions(extractions, company="Acme Corp")
print(report.summary)

# Filter out errors before Neo4j write
clean = filter_extractions(extractions, report, exclude_errors=True)
```

### Providing Domain Keywords

Pass `domain_keywords` to help future semantic checks:

```python
report = validate_extractions(
    extractions,
    company="Acme Corp",
    domain_keywords=["audio", "hifi", "speaker", "amplifier"],
)
```

This doesn't change current check behavior but is plumbed through for future LLM-based validation.

## Limitations

### Known Gaps

1. **Noise entities without keyword matches** — Entities from unrelated domains (e.g., a quantum computing company) are only caught if they contain noise keywords or their source is isolated. If a noise entity co-occurs with legitimate entities, it passes through.

2. **Type mismatch heuristic is shallow** — The person-vs-company check relies on capitalization patterns and corporate suffixes. Brand names that look like person names (e.g., "Mark Levinson", "Dan D'Agostino", "Franco Serblin") will be incorrectly flagged as warnings. Industries with many eponymous brands (audio, fashion, food) will see more false positives.

3. **No semantic understanding** — Checks are string-based. The pipeline doesn't know that a quantum computing company is unrelated to an audio trade show. A future LLM validation pass could catch this at ~$0.01 per entity.

4. **Duplicate detection is exact-normalized only** — "Audio-Technica" and "Audio Technica" won't match because hyphen handling isn't implemented.

5. **Source relevance check requires multiple sources** — With only 1–2 sources, there's no baseline to detect isolation. Most useful with 5+ diverse sources.

### Trade-offs

The pipeline intentionally uses **cheap heuristics over LLM calls**:

- **Pro:** Zero additional API cost, instant execution, deterministic results
- **Con:** Can't catch semantic noise (entities that are syntactically plausible but domain-irrelevant)

This is the right trade-off at current scale. If extraction volumes grow or higher precision is needed, add an LLM validation tier.

## Applying to New Companies

1. **Provide `domain_keywords`** when calling `validate_extractions`. This helps future semantic checks filter noise from adjacent industries.

2. **Review the validation report before trusting the graph.** The report's `summary` method gives a quick overview. Warnings are informational — they highlight entities worth a second look, not definitive errors.

3. **Expect false positives on eponymous brands.** Audio, fashion, and food industries have many brands named after people. The type mismatch check will flag these. This is a feature (prompts review) not a bug.

4. **The noise keyword list is generic.** It catches cross-industry contamination (quantum, crypto, pharma) but won't catch noise from adjacent industries. Extend `noise_keywords` in `check_noise_entities` for domain-specific filtering.

## Extending the Pipeline

- **Fuzzy duplicate matching** — Use Levenshtein distance or token set ratio for near-duplicates. Keep threshold conservative (>0.9 similarity).
- **LLM validation tier** — For high-value extractions, add an optional Claude pass that reviews flagged warnings: "Is 'Mark Levinson' a person or an audio brand?" Cost: ~$0.01 per entity.
- **Cross-extraction relationship validation** — Check that relationship endpoints actually exist as extracted entities.
- **Historical baseline** — Compare current extraction against previous runs for the same company. New entities are worth flagging.

## Validation by Extraction Tier

| Tier | Validation Value | Notes |
| --- | --- | --- |
| Regex (structured pages) | Low | Output is deterministic, but page layout changes could introduce garbage |
| Ollama (classification) | Medium | Misclassification is the main risk, type mismatch check helps |
| Claude/LLM (reasoning) | High | Unstructured sources produce the most noise — this is what validation was built for |

## Example:  Live Run

Extraction run on `ephemeral_` collection (30 chunks, Ollama/Mistral):

```text
Entities: 179 total, 172 clean, 7 flagged
Relationships: 129
Flags: 8 (0 errors, 8 warnings)
Error rate: 0.0% — pipeline continued to Neo4j write
```

All 7 warnings were type mismatch false positives on legitimate audio brands (Grand Prix Audio, Franco Serblin, etc.). Zero errors — the QphoX/Rigetti noise from previous runs did not recur.

## Source Files

| File | What |
| ---- | ---- |
| `src/.../rag/validate.py` | Validation checks and report generation |
| `src/.../rag/graph.py` | Integration point (`build_company_graph`) |
| `tests/test_validate.py` | 15 tests with synthetic noise data |
