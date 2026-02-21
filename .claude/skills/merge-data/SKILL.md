---
name: merge-data
description: "Merge monthly returns with fundamental data, handling date alignment, forward-fill, look-ahead bias, and data quality filters."
---

# Merge Data

Merges the monthly returns dataset (from `fetch-returns`) with fundamental data (from `fetch-fundamentals`), handling date alignment and look-ahead bias.

## When to Use This Skill

Use this skill when the user wants to:
- Combine monthly returns with fundamental variables
- Create a merged dataset for portfolio analysis or backtesting
- Align SEC filing dates with monthly return periods

## Usage

```bash
python .claude/skills/merge-data/scripts/merge_monthly_fundamentals.py monthly.parquet fundamentals.parquet merged.parquet
```

## What the Script Does

### 1. Aligns Fundamentals to Filing Dates
Fundamental data becomes available in the first full month **after** the SEC filing date (`datekey`). The script maps each filing to its `available_month`.

### 2. Merges on (ticker, month)
Left-joins fundamentals onto the monthly returns data.

### 3. Forward-Fills Fundamental Data
Within each ticker, fundamental values are carried forward until the next filing replaces them.

### 4. Shifts SF1 Variables by 1 Month
**CRITICAL:** After merging and forward-filling, all SF1 variables are shifted by 1 month (grouped by ticker) to avoid look-ahead bias. This ensures each row's fundamentals represent information known at the **start** of the month.

### 5. Shifts Close Price
The `close` column is shifted to represent the prior month's closing price (known at the start of the period).

### 6. Applies Data Quality Filters
- Drops rows where `close < $5.00` (penny stock filter)
- Drops rows with any missing data

## Output Format

Final dataset columns:
- `ticker`, `month`: Identifiers
- `return`: Monthly return (decimal)
- `momentum`, `lag_month`: Momentum signals
- `close`: Prior month's closing price (shifted)
- `marketcap`: Prior month's market cap (shifted in `fetch-returns`)
- `sector`, `industry`, `size`: Classifications
- All requested fundamental variables (shifted by 1 month)

## Key Rules

- **All SF1 variables are shifted by 1 month** after merging (the script handles this)
- **DAILY variables should already be shifted** before this step (handled in `fetch-fundamentals`)
- **Growth rates must be calculated before merging** (handled in `fetch-fundamentals`)
- **The `date` column is dropped** in the final output (use `month` for time identification)
- Output supports `.parquet`, `.xlsx`, or `.csv`

## Avoiding Look-Ahead Bias -- Summary

| Variable Source | When to Shift | Who Shifts It |
|----------------|---------------|---------------|
| DAILY table (pb, pe, etc.) | After fetching | `fetch-fundamentals` |
| SF1 table (roe, de, etc.) | After merging + forward-fill | `merge-data` (this script) |
| Marketcap | After fetching | `fetch-returns` |
| Close price | After merging | `merge-data` (this script) |

## Dependencies

- Requires output from `fetch-returns` (monthly returns file)
- Requires output from `fetch-fundamentals` (fundamentals file)
