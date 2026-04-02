# Decomposition Catalogs

Machine-readable YAML catalogs of vendor product decompositions into neutral functional primitives.

**Schema:** [`_schema.yaml`](_schema.yaml)
**Human-readable docs:** [`docs/research/decompositions/`](../../../docs/research/decompositions/)
**Methodology:** [`docs/research/system-primitive-decomposition.md`](../../../docs/research/system-primitive-decomposition.md)

## Catalogs

| File | Vendor | Category | Primitives |
| ---- | ------ | -------- | ---------- |
| `salesforce-crm.yaml` | Salesforce Sales Cloud | CRM | 12 |
| `zoho-crm.yaml` | Zoho CRM | CRM | 13 |
| `pipedrive-crm.yaml` | Pipedrive | CRM | 8 |
| `attio-crm.yaml` | Attio | CRM | 10 |
| `contentful-cms.yaml` | Contentful | Headless CMS | 26 |
| `wordpress-cms.yaml` | WordPress | Monolithic CMS | 16 |
| `strapi-cms.yaml` | Strapi | Headless CMS (OSS) | 14 |
| `bynder-dam.yaml` | Bynder | DAM | 16 |
| `cloudinary-dam.yaml` | Cloudinary | DAM (API-first) | 19 |
| `gmail-email.yaml` | Gmail | Email | 11 |
| `notion-workspace.yaml` | Notion | Workspace / Knowledge Mgmt | 12 |
| `airtable-database.yaml` | Airtable | Low-Code Database | 12 |
| `zapier-automation.yaml` | Zapier | Integration / Automation | 11 |

## Graph Model

These catalogs seed the Neo4j knowledge graph in semops-data:

```
(:VendorProduct)-[:DECOMPOSES_TO]->(:Primitive)
(:Primitive)-[:APQC_CONTEXT]->(:ProcessGroup)
(:VendorProduct)-[:ALTERNATIVE_TO]->(:OpenPrimitiveTool)
```
