# Industry Intelligence Sourcebook - Schema Reference

This file defines the canonical data structure shared by all industry sourcebook JSON files. Every `{industry}_sourcebook.json` must follow this schema.

## Top-level Fields

| Field | Type | Required | Description |
|:--|:--|:--|:--|
| `industry` | string | yes | Industry identifier, lowercase (e.g., "ipc", "maritime") |
| `industry_zh` | string | yes | Industry name in Chinese |
| `version` | string | yes | Semantic version of this sourcebook |
| `last_updated` | string | yes | ISO date of last update |
| `source_pyramid` | object | yes | 4-layer source hierarchy (L1-L4) |
| `competitors` | object | yes | Competitor companies grouped by priority |
| `exhibition_calendar` | array | yes | Annual exhibition schedule |
| `search_whitelist` | object | yes | Domain whitelists for 3 search tracks |
| `query_templates` | object | yes | Search query templates |
| `cross_validation` | object | yes | Cross-validation rules and mappings |
| `scoring` | object | yes | 6-dimension scoring rubric |

## source_pyramid

```
{
  "L1": {
    "weight": 3,
    "description": "一手源：厂商官方/行业标准组织/政府机构",
    "entries": [
      {
        "id": "unique-id",
        "name_zh": "中文名",
        "name_en": "English Name",
        "type": "competitor | standards_org | government | exhibition",
        "tier": "global_top | regional_top | niche",    // only for competitors
      "domain": "example.com",
      "domains": ["example.com", "example.com.cn"],  // 🆕 all regional domains for search
      "homepage": "https://www.example.com",
        "core_expos": ["expo-id-1", "expo-id-2"],       // only for competitors
        "cross_verify_required": true | false
      }
    ]
  }
}
```

## competitors

```
{
  "primary": ["list of competitor ids that are direct APQ rivals"],
  "secondary": ["list of competitor ids for broader monitoring"],
  "watch": ["list of competitor ids as emerging/new entrants"],
  "expo_trackers": {
    "advantech": {
      "verified_expos": ["embedded-world", "computex"],
      "excluded_expos": {"hannover-messe": "偏整线方案，IPC新品少", "automate": "与COMPUTEX重复"}
    }
  }
}
```

## exhibition_calendar

```
[
  {
    "id": "embedded-world",
    "name": "embedded world",
    "name_zh": "德国嵌入式工业展",
    "location": "Nuremberg, Germany",
    "month": 3,
    "priority": "P0 | P1",
    "region": "DE | CN | US",
    "domain": "embedded-world.de",
    "competitor_participation": ["advantech", "nodka", "jwi"],
    "reverse_scan_value": "IPC厂商年度新品发布主场"
  }
]
```

## search_whitelist

```
{
  "news_domestic": [list of trusted domestic domains for Chinese news search],
  "news_international": [list of trusted international domains for English news search],
  "competitor": [list of competitor official domains for competitor intelligence search]
}
```

## query_templates

```
{
  "news_cn": {
    "query": "template with {year} {month} placeholders",
    "keyword_groups": ["group1", "group2"]
  },
  "news_intl": { "query": "...", "keyword_groups": [...] },
  "competitor_scan": { "query": "...", "keyword_groups": [...] },
  "expo_season": {
    "embedded-world": "template for embedded world season",
    "hannover-messe": "...",
    "ciif": "..."
  }
}
```

## cross_validation

```
{
  "min_independent_sources": 2,
  "verification_levels": {
    "confirmed": { "icon": "✅", "description": "≥2 independent domains" },
    "single_l1": { "icon": "⚠️", "description": "Only L1 source" },
    "single_l2_l3": { "icon": "🔍", "description": "Single L2/L3 source" },
    "unverifiable": { "icon": "❌", "description": "L4 only, no other source" }
  },
  "cn_to_intl_mapping": {
    "中文厂商/术语": "English equivalent for cross-search"
  },
  "intl_to_cn_mapping": {
    "English term": "中文对应"
  }
}
```

## scoring

```
{
  "dimensions": [
    {
      "name": "timeliness",
      "name_zh": "时效性",
      "weight": 2,
      "rubric": [
        {"score": 10, "condition": "当天"},
        {"score": 9, "condition": "1天前"},
        {"score": 7, "condition": "3天前"},
        {"score": 5, "condition": "5天前"},
        {"score": 3, "condition": "≥7天"}
      ]
    }
  ],
  "max_score": 94,
  "threshold": 45,
  "cross_verify_bonus": 2
}
```

## P0 Verification Fields (v1.1.0 · 2026-07-02)

Added to every L1/L2 source entry per professional market intelligence review:

### verification
```json
{
  "verification": {
    "last_verified": "2026-07-02",
    "verified_by": "manual | auto",
    "status": "active | suspicious | deprecated",
    "credentials": ["ICP备案号", "官方认证账号"],
    "notes": "P0 upgrade 2026-07-02"
  }
}
```
Tracks source credibility: when last checked, by whom, and current trust status.

### parent_entity
```json
"parent_entity": "AspenCore"
```
Actual controlling entity. E.g. EE Times + EE Times China both belong to AspenCore → not independent. Used to prevent counting sibling domains as separate sources.

### content_type
```json
"content_type": "official_announcement"
```
Enum: `official_announcement | product_page | investor_relation | standards_document | policy_document | independent_reporting | consulting_report | press_aggregation | general_media | exhibition_listing | social_media`

Drives noise filtering and differentiates press releases from independent journalism.

### aliases
```json
"aliases": ["ADLINK Technology", "凌华科技"]
```
Name variants for entity resolution and cross-language search.

### ttl
```json
{
  "ttl": {
    "valid_until": "permanent",
    "update_frequency": "daily"
  }
}
```
Per-source collection cadence. Frequency: daily (L1 competitors), weekly (standards/media), event_driven (exhibitions).

### compliance
```json
{
  "compliance": {
    "allow_scrape": true,
    "api_available": false,
    "rate_limit": "10/min",
    "robots_txt_compliant": true,
    "data_retention_days": 90,
    "requires_auth": false,
    "jurisdiction": "DE"
  }
}
```
Legal/operational boundary for data collection from this source.

## Programmatic Validation

The canonical JSON Schema for programmatic validation is at `references/sourcebook.schema.json` (proper JSON Schema Draft 2020-12 format). Run validation with:

```bash
python validate_sourcebooks.py
```