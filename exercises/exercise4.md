# Exercise 4: Rolling Windows for Train/Test

**Session 4 topics:** Expanding-window backtesting, rolling-window backtesting, Spearman rank correlation, time-series cross-validation.

Load `merged.parquet`. Use the same ranked features and ranked target from Exercise 3.

### Submission

Submit a **Jupyter notebook** (`.ipynb`) containing all code, output, and charts for Parts (a) through (d). Use markdown cells for any written discussion.

---

## Part (a): Expanding-Window Backtest

1. Implement an **expanding-window** backtest with LightGBM (100 trees, learning rate 0.05, max depth 6).
   - Start predicting from January 2016 (train on all data before each prediction month).
   - Each month: train on all prior months, predict the current month, record predictions.
2. Each month, sort predictions into deciles and compute equal-weighted mean returns.
3. Report the time-series average of each decile's monthly return.
4. Compute and report the annualized Sharpe ratio for each decile and for the D10 - D1 long-short portfolio.
5. Plot the cumulative return of each decile portfolio.

---

## Part (b): Rolling-Window Backtest

1. Repeat Part (a) using a **rolling window** of 60 months (5 years) instead of an expanding window.
   - Each month, train only on the most recent 60 months of data.
2. Report the same statistics: decile mean returns, Sharpe ratios, and cumulative return chart.
3. Compare expanding vs. rolling window. In a markdown cell, discuss:
   - Which produces a better D10 - D1 spread?
   - Which has a higher Sharpe ratio for the long-short portfolio?

   Plot both long-short cumulative return series on a single chart.

---

## Part (c): Monthly Spearman Rank Correlation

For each prediction month in the expanding-window backtest:

1. Compute the **Spearman rank correlation** between predicted ranks and actual return ranks.
2. Plot the monthly Spearman correlations over time as a time-series chart.
3. Report the mean, median, standard deviation, and fraction of months with positive correlation.
4. Identify the 3 months with the highest and lowest Spearman correlations. In a markdown cell, discuss whether there are any patterns (e.g., market stress periods).
5. Repeat for the rolling-window backtest and overlay both Spearman series on the same plot.

---

## Part (d): Time-Series Cross-Validation

Demonstrate time-series CV for hyperparameter selection on a single prediction date (January 2020):

1. Define the training window as all data before January 2020.
2. Create 5 time-series folds within the training window:
   - Fold 1: Train through 2014, validate on 2015
   - Fold 2: Train through 2015, validate on 2016
   - Fold 3: Train through 2016, validate on 2017
   - Fold 4: Train through 2017, validate on 2018
   - Fold 5: Train through 2018, validate on 2019
3. For each fold, train LightGBM with three different max-depth values (3, 5, 7) and compute the Spearman correlation on the validation set.
4. Report the average Spearman across folds for each max-depth. In a markdown cell, state which depth performs best.
5. In a markdown cell, discuss whether the improvement from CV is large enough to justify the computational cost.
