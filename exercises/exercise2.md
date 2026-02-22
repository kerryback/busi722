# Exercise 2: Fundamental Indicators and Merging

**Session 2 topics:** Rice Data Portal pipeline, SF1 fundamentals, look-ahead bias, data quality filters, cross-sectional standardization.

Use Claude Code with the `fetch-returns`, `fetch-fundamentals`, and `merge-data` skills. Fundamental data comes from the SF1 table.

### Submission

Submit a **Jupyter notebook** (`.ipynb`) containing all code, output, and charts for Parts (a) through (d). Use markdown cells for any written discussion. Also submit the **`merged.parquet`** file produced in Part (c). Include at least one **screenshot** of your Claude Code session showing the use of a data skill.

---

## Part (a): Build the Monthly Returns Dataset

Using the Rice Data Portal, fetch monthly returns data for all stocks from January 2022 through the most recent available month.

1. Report the total number of rows, unique tickers, and date range.
2. How many rows are lost when you apply the penny-stock filter (drop rows with `close` < $5)?
3. What fraction of stock-months have missing `momentum`? In a markdown cell, explain why momentum is missing for early observations.

---

## Part (b): Fetch and Compute Fundamentals

Fetch annual fundamentals from the SF1 table for all stocks. At minimum, retrieve: `assets`, `equity`, `gp` (gross profit), `roe`, `grossmargin`, `assetturnover`, and `de` (debt-to-equity).

1. Compute `asset_growth` as the year-over-year percentage change in `assets`. **Important:** compute this *before* merging with returns. In a markdown cell, explain why this ordering matters.
2. Compute `gp_to_assets` = `gp / assets`.
3. Report the number of unique tickers and the date range in the fundamentals data.
4. Display summary statistics for `roe`, `grossmargin`, `asset_growth`, and `gp_to_assets`.

---

## Part (c): Data Quality Checks

Merge the monthly returns with fundamentals and save as `merged.parquet`. Using the merged dataset:

1. For each fundamental variable, report the fraction of stock-months where the variable is non-missing.
2. Compute the cross-sectional mean and standard deviation of `roe`, `gp_to_assets`, and `asset_growth` for each month. Plot these over time. In a markdown cell, discuss whether the means are stable or show trends.
3. Check for extreme outliers: what fraction of `roe` values are above 1.0 or below -1.0? What fraction of `asset_growth` values are above 5.0?
4. Report the final dataset's shape and column list.

---

## Part (d): Size and Value Sorts

Using the merged dataset, `marketcap` measures size and `pb` (price-to-book from the DAILY table) measures valuation. Book-to-market is the inverse: $\text{B/M} = 1 / \text{pb}$.

1. Each month, sort stocks into **quintiles** by `marketcap`. Compute the equal-weighted mean return for each quintile. Report the time-series average. In a markdown cell, discuss whether small stocks outperform large stocks.
2. Each month, sort stocks into **quintiles** by book-to-market ($1/\text{pb}$). Compute the equal-weighted mean return for each quintile. Report the time-series average. In a markdown cell, discuss whether value stocks (high B/M) outperform growth stocks (low B/M).
3. Perform a **double sort**: each month, independently sort stocks into **size terciles** (3 groups by `marketcap`) and **B/M terciles** (3 groups by $1/\text{pb}$). Form the $3 \times 3 = 9$ portfolios. Compute the equal-weighted mean return for each portfolio and display as a table (rows = size, columns = B/M).
4. Create a bar chart showing the mean monthly return for each size quintile.
5. In a markdown cell, discuss whether the value premium (high B/M minus low B/M) is stronger among small stocks or large stocks.
