---
name: rice-data-query
description: "Database access and query patterns for the Rice Data Portal. Foundation skill for all data fetching."
---

# Rice Data Query

Provides connection setup, SQL patterns, and schema reference for the Rice Data Portal database.

## When to Use This Skill

Use this skill when:
- Connecting to the Rice Data Portal API
- Writing SQL queries against SEP, DAILY, SF1, or TICKERS tables
- Checking which variables are precomputed vs. need manual calculation

## Connection Setup

**API Endpoint:** `https://data-portal.rice-business.org/api/query`
**Authentication:** Bearer token from `RICE_ACCESS_TOKEN` in `.env`

```python
import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
ACCESS_TOKEN = os.getenv('RICE_ACCESS_TOKEN')
API_URL = "https://data-portal.rice-business.org/api/query"

response = requests.post(
    API_URL,
    headers={"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"},
    json={"query": sql},
    timeout=120
)
```

## Database Schema

Full schema documentation is in `.claude/skills/rice-data-query/rice_database_schema.md`. Key tables:

### TICKERS Table
One row per stock: `ticker`, `name`, `sector`, `industry`, `exchange`, `scalemarketcap`, `isdelisted`

### SEP Table (Daily Prices)
Daily price data: `ticker`, `date` (VARCHAR), `open`, `high`, `low`, `close`, `closeadj`, `volume`

**CRITICAL:** `close` is a SQL reserved keyword. Always use a table alias: `SELECT a.close FROM sep a`

### DAILY Table (Daily Valuation Metrics)
`ticker`, `date` (VARCHAR), `marketcap` (in thousands), `pb`, `pe`, `ps`, `ev`, `evebit`, `evebitda`

### SF1 Table (Fundamentals from SEC Filings)
**SF1 has NO `date` column.** Use `reportperiod`, `datekey`, or `calendardate`.

Dimensions (always use AR):
- `ARY` = Annual (10-K), `ARQ` = Quarterly (10-Q), `ART` = Trailing 12 months
- **NEVER** use MR dimensions (contain restatements)

## Checking Precomputed Variables

**CRITICAL:** Before calculating any financial ratio, check if it already exists in the database.

```bash
python .claude/skills/rice-data-query/scripts/check_precomputed.py pb,roe,asset_growth
```

Common precomputed ratios:
- **DAILY:** `marketcap`, `pb`, `pe`, `ps`, `ev`, `evebit`, `evebitda`
- **SF1:** `roe`, `roa`, `roic`, `grossmargin`, `netmargin`, `ebitdamargin`, `de`, `assetturnover`, `currentratio`, `divyield`, `payoutratio`

**Rule:** Fetch precomputed ratios from the database. Do NOT calculate manually if they exist.

## SQL Rules

1. **Only SELECT statements**
2. **All date columns are VARCHAR** -- must cast: `date::DATE`, `reportperiod::DATE`
3. **Query year-by-year** to avoid API timeouts
4. **Always ORDER BY** `ticker, date` or `ticker, datekey`

## Common Query Patterns

### End-of-Month Values (SEP or DAILY)

```sql
WITH month_ends AS (
  SELECT a.ticker, a.date::DATE as date, a.close, a.closeadj,
         ROW_NUMBER() OVER (
           PARTITION BY a.ticker, DATE_TRUNC('month', a.date::DATE)
           ORDER BY a.date::DATE DESC
         ) as rn
  FROM sep a
  WHERE a.date::DATE >= '{year}-01-01'
    AND a.date::DATE < '{year+1}-01-01'
)
SELECT ticker, date, close, closeadj
FROM month_ends WHERE rn = 1
ORDER BY ticker, date
```

### SF1 Fundamental Data

```sql
SELECT ticker, reportperiod, datekey, equity, assets, debt, roe, grossmargin
FROM sf1
WHERE dimension = 'ARY'
  AND reportperiod::DATE >= '{year}-01-01'
  AND reportperiod::DATE < '{year+1}-01-01'
ORDER BY ticker, datekey
```

## Scripts

- `scripts/check_precomputed.py` -- Check which variables exist in DAILY/SF1
- `scripts/precomputed_variables.py` -- Master list of all precomputed variables with aliases
- `rice_database_schema.md` -- Complete database schema reference
