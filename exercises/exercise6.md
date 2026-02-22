# Exercise 6: Costs, Risk, and Drawdowns

**Session 6 topics:** Transaction costs, turnover, drawdowns, underwater charts, alternative portfolio weighting, covariance estimation.

Use the portfolio returns and weight series from Exercise 5. Load `merged.parquet` for any additional computations.

### Submission

Submit a **Jupyter notebook** (`.ipynb`) containing all code, output, and charts for Parts (a) through (d). Use markdown cells for any written discussion.

---

## Part (a): Turnover and Transaction Cost Analysis

1. For the **linear-weight long-short** portfolio (Exercise 5, Part b), compute the monthly **turnover**: $\text{turnover}_t = \sum_i |w_{i,t} - w_{i,t-1}^+|$ where $w_{i,t-1}^+$ is the drift-adjusted weight from the prior month.
2. Report the mean, median, and maximum monthly turnover.
3. Estimate net-of-cost returns under three cost scenarios:
   - **Low cost:** 5 bps per unit of turnover (institutional)
   - **Medium cost:** 20 bps per unit of turnover
   - **High cost:** 50 bps per unit of turnover
4. For each scenario, report the net Sharpe ratio of the long-short portfolio. In a markdown cell, discuss at what cost level the strategy becomes unprofitable.
5. Plot gross vs. net cumulative returns for all three cost scenarios.

---

## Part (b): Drawdown Analysis

For the long-short linear-weight portfolio:

1. Compute the **drawdown** series: $\text{dd}_t = (V_t - V_{\max,t}) / V_{\max,t}$ where $V_t$ is the cumulative portfolio value.
2. Report the **maximum drawdown**, its start date, trough date, and recovery date (if recovered).
3. Report the 5 worst monthly returns and the 5 largest drawdowns.
4. Plot the **underwater chart** (drawdown over time).
5. Repeat for the long-only top-decile portfolio. In a markdown cell, discuss which portfolio has deeper drawdowns and why.

---

## Part (c): Alternative Weighting Schemes

Compare three long-only portfolio weighting approaches applied to the top-quintile predicted stocks:

1. **Equal-weighted:** $w_i = 1/n$ for top-quintile stocks.
2. **Market-cap weighted:** $w_i \propto \text{mcap}_i$ for top-quintile stocks.
3. **Inverse-volatility weighted:** $w_i \propto 1 / \hat{\sigma}_i$ for top-quintile stocks, where $\hat{\sigma}_i$ is the trailing 12-month return standard deviation.

For each weighting scheme, compute monthly portfolio returns and report:
- Mean monthly return, annualized volatility, annualized Sharpe ratio
- Maximum drawdown
- Average number of stocks with weight > 2%

Plot the cumulative returns of all three weighting schemes on a single chart. In a markdown cell, discuss which scheme offers the best risk-adjusted performance.

---

## Part (d): Ledoit-Wolf Shrinkage and Minimum-Variance Portfolios

The sample covariance matrix is noisy when the number of stocks is large relative to the number of time periods. Ledoit-Wolf shrinkage blends the sample covariance with a structured target to reduce estimation error.

1. From the merged dataset, select all **Technology sector** stocks that have complete monthly return data from January 2019 through December 2024. Use 2019-2021 as the **estimation window** and 2022-2024 as the **evaluation window**. Report how many stocks are in this universe.
2. Using the estimation window, compute the **sample covariance matrix** and the **Ledoit-Wolf shrinkage covariance matrix** (use `sklearn.covariance.LedoitWolf`). Report the shrinkage intensity $\delta$.
3. Using each covariance matrix, compute the **minimum-variance portfolio** (fully invested, long-only: $\mathbf{w}'\mathbf{1} = 1$, $w_i \ge 0$). Report the number of stocks with nonzero weight and the maximum weight for each.
4. Evaluate both minimum-variance portfolios **out of sample** (2022-2024). Report the annualized realized volatility and Sharpe ratio for each. Also report results for an equal-weighted portfolio of the same stocks as a benchmark. Plot the cumulative returns of all three portfolios over the evaluation window.
