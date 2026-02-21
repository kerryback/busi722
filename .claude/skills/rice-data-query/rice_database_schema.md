# Rice Data Portal Database Schema

This reference provides complete schema documentation for the Rice Data Portal database, shared across all data analysis skills.

## Connection Setup

**API Endpoint:** `https://data-portal.rice-business.org/api/query`
**Authentication:** Bearer token from environment variable `RICE_ACCESS_TOKEN`

**Python connection code:**
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

---

## Database Tables

### TICKERS Table

**One row per stock - permanent company information**

Core columns:
- `ticker`: Stock symbol
- `name`: Company name
- `sector`, `industry`: Classifications
- `exchange`: NYSE, NASDAQ, NYSEMKT (case-sensitive)
- `scalemarketcap`: '1 - Nano', '2 - Micro', '3 - Small', '4 - Mid', '5 - Large', '6 - Mega'
- `isdelisted`: Y or N

---

### SEP Table (Stock End-of-Day Prices)

**Daily price data**

Core columns:
- `ticker`, `date` (VARCHAR - must cast to DATE)
- `open`, `high`, `low`, `close` (split-adjusted)
- `volume`
- `closeadj`: Close price adjusted for splits, dividends, spinoffs

**⚠️ CRITICAL:** `close` is SQL reserved keyword, use alias: `SELECT a.close FROM sep a`

---

### DAILY Table (Daily Valuation Metrics)

**Daily valuation metrics calculated from prices and fundamentals**

All columns:
- `ticker`, `date` (VARCHAR - must cast to DATE)
- `marketcap`: Market capitalization (**in thousands of USD**)
- `pb`: Price-to-book ratio
- `pe`: Price-to-earnings ratio
- `ps`: Price-to-sales ratio
- `ev`: Enterprise value (millions)
- `evebit`: EV / EBIT ratio
- `evebitda`: EV / EBITDA ratio

**⚠️ IMPORTANT:** `marketcap` values are in thousands. To convert to millions: `marketcap / 1000`

---

### SF1 Table (Fundamentals from 10-K/10-Q)

**Financial statement data from SEC filings**

**⚠️ CRITICAL:** SF1 has NO 'date' column! Use `reportperiod`, `datekey`, or `calendardate`.

#### Key Columns

- `ticker`
- `dimension`: ARY (annual), ARQ (quarterly), ART (trailing 12 months) - **ALWAYS use AR dimensions**
- `reportperiod`: Fiscal period end date (e.g., "2024-12-31") - **primary date field**
- `datekey`: SEC filing date
- `fiscalperiod`: Fiscal period name (e.g., "2024-Q4")

#### Income Statement

- `revenue`, `cor` (cost of revenue), `gp` (gross profit)
- `sgna`, `rnd`, `opex` (operating expenses)
- `opinc` (operating income), `ebit`, `ebitda`
- `intexp` (interest expense), `taxexp`
- `netinc`, `netinccmn` (to common shareholders)
- `eps`, `epsdil`, `shareswa`, `shareswadil`

#### Balance Sheet

- `assets`, `assetsc` (current assets), `assetssc` (non-current)
- `cashneq`, `inventory`, `receivables`, `ppnenet`
- `liabilities`, `liabilitiesc`, `liabilitiesnc`
- `debt`, `debtc`, `debtnc`
- `equity`, `retearn`, `accoci`

#### Cash Flow

- `ncfo`, `ncfi`, `ncff`, `ncf`
- `capex`, `fcf`, `depamor`, `sbcomp`

#### Financial Ratios (pre-calculated)

**⚠️ IMPORTANT: These ratios are already computed in both DAILY and SF1 tables. Check for their availability before calculating manually.**

- `roe`, `roa`, `roic`, `ros`
- `grossmargin`, `netmargin`, `ebitdamargin`
- `currentratio`, `quickratio`
- `de` (debt-to-equity ratio - this is "leverage")
- `assetturnover`
- `payoutratio`, `divyield`
- `pe`, `pb`, `ps`

**⚠️ All SF1 values are in absolute dollars** (not thousands or millions)

---

## SQL Query Rules

### Basic Rules

1. **Only SELECT statements** - no other SQL operations
2. **SF1 has NO 'date' column** - use `reportperiod`, `datekey`, or `calendardate`
3. **All date columns are VARCHAR** - must cast: `reportperiod::DATE`, `date::DATE`
4. **Only reference tables/columns that exist** in the schema above

### Date Handling

**All date comparisons require casting:**
```sql
WHERE date::DATE >= '2020-01-01'
WHERE reportperiod::DATE >= CURRENT_DATE - INTERVAL '5 years'
```

**DuckDB date intervals:**
```sql
INTERVAL '2 years'    -- correct
INTERVAL '6 months'   -- correct
```

### SF1 Dimensions

**ALWAYS use AR (As Reported) dimensions:**
- `ARY` = As Reported Annual (10-K filings)
- `ARQ` = As Reported Quarterly (10-Q filings)
- `ART` = As Reported Trailing 12 months

**NEVER use MR dimensions** (contain restatements)

**SF1 queries must include:**
```sql
SELECT ticker, reportperiod, datekey, [variables]
FROM sf1
WHERE dimension = 'ARY'
  AND reportperiod::DATE >= '2020-01-01'
ORDER BY ticker, datekey  -- CRITICAL: always order by ticker, datekey
```

---

## Common Query Patterns

### End-of-Month Prices (SEP Table)

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
FROM month_ends
WHERE rn = 1
ORDER BY ticker, date
```

### End-of-Week Prices (SEP Table)

```sql
WITH week_ends AS (
  SELECT a.ticker, a.date::DATE as date, a.close, a.closeadj,
         ROW_NUMBER() OVER (
           PARTITION BY a.ticker, DATE_TRUNC('week', a.date::DATE)
           ORDER BY a.date::DATE DESC
         ) as rn
  FROM sep a
  WHERE a.date::DATE >= '{year}-01-01'
    AND a.date::DATE < '{year+1}-01-01'
)
SELECT ticker, date, close, closeadj
FROM week_ends
WHERE rn = 1
ORDER BY ticker, date
```

### Fetch DAILY Table Variables

```sql
WITH month_ends AS (
  SELECT d.ticker, d.date::DATE as date, d.pb, d.pe, d.marketcap,
         ROW_NUMBER() OVER (
           PARTITION BY d.ticker, DATE_TRUNC('month', d.date::DATE)
           ORDER BY d.date::DATE DESC
         ) as rn
  FROM daily d
  WHERE d.date::DATE >= '{year}-01-01'
    AND d.date::DATE < '{year+1}-01-01'
)
SELECT ticker, CAST(date AS VARCHAR) as date, pb, pe, marketcap
FROM month_ends
WHERE rn = 1
ORDER BY ticker, date
```

### Fetch SF1 Fundamental Data

```sql
SELECT ticker, reportperiod, datekey, equity, assets, debt, roe, grossmargin, assetturnover, de
FROM sf1
WHERE dimension = 'ARY'
  AND reportperiod::DATE >= '{year}-01-01'
  AND reportperiod::DATE < '{year+1}-01-01'
ORDER BY ticker, datekey
```

---

## Important Notes

1. **Query year-by-year** - Avoid API timeouts by breaking queries into yearly chunks
2. **Always order results** - Use `ORDER BY ticker, date` or `ORDER BY ticker, datekey`
3. **Check for precomputed ratios** - Many financial ratios exist in DAILY and SF1
4. **Forward fill fundamentals** - SF1 data propagates until next filing
5. **Shift for look-ahead bias** - Shift variables by appropriate period after fetching

---

## External Documentation

- [Rice Data Portal Guide](https://portal-guide.rice-business.org)
- [Rice Data Portal API](https://data-portal.rice-business.org)
