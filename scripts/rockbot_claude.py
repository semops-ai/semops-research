"""Run  enrichment via Claude API for quality comparison."""
import logging
logging.getLogger("research_toolkit").setLevel(logging.ERROR)

from research_toolkit.diligence import Classification, generate_reference

c = Classification(
    customer_type="b2b",
    sector="enterprise_software",
    industry="vertical_saas",
)

ref = generate_reference(
    c,
    enrich=True,
    enrichment_provider="anthropic",
    company_name="",
    company_url="https://.com",
)

meta = ref.metadata
derived = meta.get("classification_derived_fields", {})

print("=== Enrichment Metadata ===")
print(f'  provider: {meta.get("enrichment_provider")} / {meta.get("enrichment_model")}')
print(f'  elapsed: {meta.get("enrichment_elapsed_seconds", 0):.1f}s')
print(f'  from_cache: {meta.get("enrichment_from_cache")}')
print(f'  urls_fetched: {meta.get("urls_fetched", [])}')
print()
print("=== Classification Derived ===")
for k, v in derived.items():
    print(f"  {k}: {v}")
print()

static = [e for e in ref.entities if e.framework_source != "llm-enrichment"]
llm_ents = [e for e in ref.entities if e.framework_source == "llm-enrichment"]
print(f"=== Results: {len(ref.entities)} entities ({len(static)} static + {len(llm_ents)} LLM), {len(ref.domain_contexts)} contexts ===")
print()

if llm_ents:
    print("--- LLM Vertical Entities ---")
    for e in llm_ents:
        print(f"  - {e.name} [{e.category}] ({e.domain_type.value})")
    print()

print("--- Domain Contexts ---")
for ctx in ref.domain_contexts:
    ent_names = [e.name for e in ctx.entities]
    rationale = ctx.rationale[:150] if ctx.rationale else "(none)"
    print(f"  [{ctx.domain_type.value.upper():10}] {ctx.name}")
    print(f"               {rationale}")
    print(f"               Entities: {ent_names}")
    print()
