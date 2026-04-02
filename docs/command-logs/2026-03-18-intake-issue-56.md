# Intake Log: Issue  — Agentic vendor product decomposition slash command

> **Command:** /intake
> **Date:** 2026-03-18
> **Target:** 
> **Related Session:** None (no prior `/issue` invocation)

## Analysis

### Territory Map

**Entity References Found**
- Pattern `system-primitive-decomposition` (1p, active) — the decomposition methodology this command automates
- Capability `vendor-decomposition` (in_progress, P31) — delivered by semops-research, implements `system-primitive-decomposition` + 3 others
- Project 31 — Due Diligence Engine. Vendor decomposition catalogs listed as "Delivered" reference data
- Methodology doc: `brand-to-neutral-decomposition.md` — 6-step process (capability extraction → primitive naming → APQC context → protocol ID → lock-in analysis → validation)

**Capability → Pattern Coverage**

| Capability | Patterns | Gap? |
|-----------|----------|------|
| `vendor-decomposition` | `system-primitive-decomposition`, `explicit-architecture`, `explicit-enterprise`, `data-system-classification` | No |

**Existing Coverage**
- 13 vendor product YAML catalogs in `data/catalogs/decompositions/`
- 10 markdown docs in `docs/research/decompositions/` (3 catalogs lack markdown docs)
- 3 cross-product analyses (CRM 4 products, CMS 3 products, DAM 2 products)
- `_schema.yaml` defines the YAML structure
- `brand-to-neutral-decomposition.md` defines the methodology end-to-end
- No existing slash commands for decomposition — all 13 catalogs were created manually

### Delta

- **Extends existing:** Automates the manual "Adding a New Decomposition" workflow as a slash command. The methodology, schema, and output format all exist — this wraps them in an agentic process.
- **Fills gap:** No agentic/automated path to produce decompositions currently exists. Each of the 13 catalogs required a full manual session.
- **Conflicts with:** Nothing.
- **Net new:** Cross-product analysis generation as part of the same command (currently written as separate manual efforts).

## Result

**Goal:** `/decompose` slash command — research vendor products, produce YAML catalogs + markdown docs + cross-product analysis, staged for human review
**Pattern Matches:** `system-primitive-decomposition` (1p, active)
**Capability Matches:** `vendor-decomposition` (in_progress, P31)
**Recommended Change Type:** Extension (new tooling for existing capability)
**Delta Summary:** Automates the existing brand-to-neutral decomposition methodology as a Claude Code slash command. All inputs (methodology, schema, output format, exemplars) already exist — this is process automation, not new methodology.

## Follow-Up

- Create `/decompose` slash command at `~/.claude/commands/decompose.md`
- Add as child issue to Project 31 execution sequence
- Link to  (methodology) and  (catalog ingestion consumer)
