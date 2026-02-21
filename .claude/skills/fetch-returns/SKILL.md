---
name: fetch-returns
description: "Fetch monthly end-of-month prices and calculate returns, momentum, and size from the Rice Data Portal."
---

# Fetch Monthly Returns

Fetches end-of-month prices from the Rice Data Portal and calculates returns, momentum, and market cap categories.

## When to Use This Skill

Use this skill when the user requests:
- Monthly stock returns or prices
- End-of-month price data
- A base monthly dataset for analysis or backtesting

## Usage

```bash
# All stocks (includes delisted to avoid survivorship bias)
python .claude/skills/fetch-returns/scripts/fetch_monthly_data.py 2020-01-01 monthly.parquet

# Specific tickers
python .claude/skills/fetch-returns/scripts/fetch_monthly_data.py AAPL,MSFT 2020-01-01 monthly.parquet
```

## What It Produces

The script automatically fetches and calculates:

| Column | Description |
|--------|-------------|
| `ticker` | Stock symbol |
| `month` | Month label (YYYY-MM) |
| `date` | End-of-month date |
| `close` | Split-adjusted closing price |
| `return` | Monthly return (decimal: 0.05 = 5%) |
| `momentum` | 12-month momentum (month t-13 to t-2) |
| `lag_month` | Prior month's return |
| `marketcap` | Market cap in thousands (shifted by 1 month) |
| `sector` | Sector classification |
| `industry` | Industry classification |
| `size` | Nano-Cap through Mega-Cap (based on marketcap percentiles) |

## How It Works

1. Fetches ticker metadata (sector, industry) from TICKERS table
2. Queries SEP table year-by-year for end-of-month prices
3. Queries DAILY table year-by-year for end-of-month marketcap
4. Merges SEP and DAILY on (ticker, date)
5. Calculates return, momentum, and lagged return (grouped by ticker)
6. Shifts marketcap by 1 month to avoid look-ahead bias
7. Assigns size categories based on cross-sectional marketcap percentiles

## Key Rules

- **Returns are decimals** (0.05 = 5%), rounded to 4 decimal places
- **Always group by ticker** when calculating returns
- **Marketcap is shifted** by 1 month (represents prior month's value)
- **Includes delisted stocks** by default to avoid survivorship bias
- **Queries year-by-year** to avoid API timeouts
- Output supports `.parquet`, `.xlsx`, or `.csv`

## Dependencies

- Requires `rice-data-query` skill for database connection (`.env` with `RICE_ACCESS_TOKEN`)
