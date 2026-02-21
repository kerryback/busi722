---
name: fetch-fundamentals
description: "Fetch fundamental data from SF1 and DAILY tables, with proper handling of precomputed ratios and growth rates."
---

# Fetch Fundamentals

Guides fetching fundamental data from the Rice Data Portal's SF1 and DAILY tables, including precomputed ratios and growth rate calculations.

## When to Use This Skill

Use this skill when the user requests:
- Fundamental data (financial ratios, balance sheet items, income statement data)
- Valuation ratios (pb, pe, ps, ev/ebitda)
- Growth rates (asset growth, revenue growth, etc.)
- Any SF1 or DAILY table variables beyond what `fetch-returns` provides

## Workflow

### Step 1: Check for Precomputed Variables

**CRITICAL:** Before calculating any ratio, check if it's precomputed.

```bash
python .claude/skills/rice-data-query/scripts/check_precomputed.py pb,roe,asset_growth,leverage
```

If a variable is precomputed, fetch it from the database. Do NOT calculate manually.

### Step 2A: Fetch from DAILY Table (Precomputed Ratios)

For variables like `pb`, `pe`, `ps`, `ev`, `evebit`, `evebitda`:

```python
# Get end-of-month values, query year-by-year
for year in range(start_year, end_year + 1):
    sql = f"""
    WITH month_ends AS (
      SELECT d.ticker, d.date::DATE as date, d.pb, d.pe,
             ROW_NUMBER() OVER (
               PARTITION BY d.ticker, DATE_TRUNC('month', d.date::DATE)
               ORDER BY d.date::DATE DESC
             ) as rn
      FROM daily d
      WHERE d.date::DATE >= '{year}-01-01'
        AND d.date::DATE < '{year+1}-01-01'
    )
    SELECT ticker, CAST(date AS VARCHAR) as date, pb, pe
    FROM month_ends WHERE rn = 1
    ORDER BY ticker, date
    """
```

**CRITICAL:** Shift DAILY variables by 1 month after fetching:
```python
df['pb'] = df.groupby('ticker')['pb'].shift(1)
df['pe'] = df.groupby('ticker')['pe'].shift(1)
```

### Step 2B: Fetch from SF1 Table (Fundamental Data)

For income statement, balance sheet, cash flow, and SF1 ratios:

```python
sql = f"""
SELECT ticker, reportperiod, datekey, equity, assets, debt, roe, grossmargin, de
FROM sf1
WHERE dimension = 'ARY'
  AND reportperiod::DATE >= '{year}-01-01'
  AND reportperiod::DATE < '{year+1}-01-01'
ORDER BY ticker, datekey
"""
```

- Use `ARY` for annual data, `ARQ` for quarterly
- Always include `reportperiod` and `datekey`
- Always `ORDER BY ticker, datekey`

### Step 3: Calculate Growth Rates BEFORE Merging

**CRITICAL:** Growth rates must be calculated from the fundamental data BEFORE merging with returns. After merging, forward-fill creates duplicate rows that produce zero growth.

```python
# Year-over-year growth for annual data
df_fund['asset_growth'] = df_fund.groupby('ticker')['assets'].pct_change().round(4)
df_fund['revenue_growth'] = df_fund.groupby('ticker')['revenue'].pct_change().round(4)

# Quarter-over-quarter for quarterly data
df_fund['revenue_growth_q'] = df_fund.groupby('ticker')['revenue'].pct_change().round(4)
```

## Output

Save the fundamental data as a parquet file. It should include:
- `ticker`
- `reportperiod` and `datekey` (for merging alignment)
- All requested fundamental variables
- Any calculated growth rates

This file is then passed to the `merge-data` skill.

## Key Rules

- **Check precomputed first** -- never manually calculate what exists in the database
- **Shift DAILY variables by 1 month** after fetching (grouped by ticker)
- **Calculate growth rates BEFORE merging** -- forward-fill breaks growth calculations
- **Query year-by-year** to avoid API timeouts
- **Always use AR dimensions** (ARY, ARQ, ART), never MR
- **SF1 has no `date` column** -- use `reportperiod` or `datekey`
- **SF1 values are in absolute dollars** (not thousands or millions)
- **DAILY `marketcap` is in thousands**

## Dependencies

- Requires `rice-data-query` skill for database connection and schema reference
