"""
Merge monthly returns data with fundamental data.
Usage: python merge_monthly_fundamentals.py MONTHLY_FILE FUNDAMENTALS_FILE OUTPUT_FILE
Example: python merge_monthly_fundamentals.py monthly.parquet fundamentals.parquet merged.parquet
"""
import sys
import pandas as pd
import numpy as np

def merge_monthly_fundamentals(monthly_file, fundamentals_file, output_file):
    """Merge monthly returns with fundamentals, handling date alignment properly."""

    print(f"Loading monthly returns data from {monthly_file}...")
    df_monthly = pd.read_excel(monthly_file) if monthly_file.endswith('.xlsx') else \
                pd.read_parquet(monthly_file) if monthly_file.endswith('.parquet') else \
                pd.read_csv(monthly_file)

    print(f"Loading fundamentals data from {fundamentals_file}...")
    df_fund = pd.read_excel(fundamentals_file) if fundamentals_file.endswith('.xlsx') else \
              pd.read_parquet(fundamentals_file) if fundamentals_file.endswith('.parquet') else \
              pd.read_csv(fundamentals_file)

    print(f"\nMonthly returns: {len(df_monthly)} rows, {df_monthly['ticker'].nunique()} tickers")
    print(f"Fundamentals: {len(df_fund)} rows, {df_fund['ticker'].nunique()} tickers")

    # STEP 1: Prepare Monthly Returns Data
    df_monthly['date'] = pd.to_datetime(df_monthly['date'])
    df_monthly = df_monthly.sort_values(['ticker', 'date']).reset_index(drop=True)

    # Shift close to represent prior period's closing price
    df_monthly['close'] = df_monthly.groupby('ticker')['close'].shift(1)

    # STEP 2: Prepare Fundamental Data
    df_fund['datekey'] = pd.to_datetime(df_fund['datekey'])

    # Calculate first month AFTER filing date
    # Add one month to filing date to get the first month when data is available
    df_fund['filing_month'] = df_fund['datekey'].dt.strftime('%Y-%m')
    df_fund['available_month_start'] = df_fund['datekey'] + pd.offsets.MonthBegin(1)
    df_fund['month'] = df_fund['available_month_start'].dt.strftime('%Y-%m')

    print("\nSample fundamental availability dates:")
    print(df_fund[['ticker', 'datekey', 'filing_month', 'month']].head(10).to_string(index=False))

    # STEP 3: Perform the Merge
    fund_columns = [col for col in df_fund.columns
                    if col not in ['reportperiod', 'datekey', 'filing_month', 'available_month_start']]

    print(f"\nMerging on (ticker, month)...")
    print(f"Fundamental columns to merge: {[c for c in fund_columns if c not in ['ticker', 'month']]}")

    df_merged = pd.merge(
        df_monthly,
        df_fund[fund_columns],
        on=['ticker', 'month'],
        how='left'
    )

    print(f"Initial merge: {len(df_merged)} rows")
    print(f"Columns after merge: {list(df_merged.columns)}")

    # Check how many rows have fundamentals
    fund_vars = [c for c in fund_columns if c not in ['ticker', 'month']]
    if fund_vars:
        first_fund_var = fund_vars[0]
        if first_fund_var in df_merged.columns:
            print(f"Rows with fundamentals: {df_merged[first_fund_var].notna().sum()}")

    df_merged = df_merged.sort_values(['ticker', 'month']).reset_index(drop=True)

    # STEP 4: Forward fill fundamental data within each ticker
    fundamental_vars = [col for col in fund_columns if col not in ['ticker', 'month']]
    print(f"\nForward filling fundamental data by ticker...")
    df_merged[fundamental_vars] = df_merged.groupby('ticker')[fundamental_vars].ffill()

    if fundamental_vars:
        first_fund_var = fundamental_vars[0]
        if first_fund_var in df_merged.columns:
            print(f"After forward fill - Rows with fundamentals: {df_merged[first_fund_var].notna().sum()}")

    # STEP 5: Shift all SF1 variables by 1 month (grouped by ticker) to avoid look-ahead bias
    # Similar to weekly-analysis skill: ALL SF1 variables must be shifted by 1 month after merging
    print(f"\nShifting SF1 variables by 1 month (grouped by ticker) to avoid look-ahead bias...")
    for var in fundamental_vars:
        df_merged[var] = df_merged.groupby('ticker')[var].shift(1)
        print(f"  Shifted {var}")

    # Calculate pb (price-to-book ratio) if equity is present
    # NOTE: pb is calculated AFTER shifting equity, so it uses prior month's equity
    if 'equity' in df_merged.columns and 'marketcap' in df_merged.columns:
        print("\nCalculating pb (price-to-book ratio) from shifted equity...")
        df_merged['pb'] = (df_merged['marketcap'] / (df_merged['equity'] / 1000)).round(4)
        df_merged.loc[df_merged['equity'] <= 0, 'pb'] = np.nan

    # STEP 6: Apply data quality filters
    initial_rows = len(df_merged)

    # Filter 1: Drop rows with close < 5.00
    print(f"\nApplying data quality filters...")
    print(f"  Initial rows: {initial_rows:,}")
    df_merged = df_merged[df_merged['close'] >= 5.00]
    print(f"  After close >= $5.00 filter: {len(df_merged):,} rows ({initial_rows - len(df_merged):,} dropped)")

    # Filter 2: Drop rows with any missing data
    rows_before_dropna = len(df_merged)
    df_merged = df_merged.dropna()
    print(f"  After dropping missing data: {len(df_merged):,} rows ({rows_before_dropna - len(df_merged):,} dropped)")
    print(f"  Total rows dropped: {initial_rows - len(df_merged):,}")

    # Drop date column
    df_merged = df_merged.drop(columns=['date'])

    # Save
    if output_file.endswith('.parquet'):
        df_merged.to_parquet(output_file, index=False)
    elif output_file.endswith('.xlsx'):
        df_merged.to_excel(output_file, index=False)
    elif output_file.endswith('.csv'):
        df_merged.to_csv(output_file, index=False)
    else:
        raise ValueError("Output file must end with .parquet, .xlsx, or .csv")

    print(f"\nMerged data saved to {output_file}")
    print(f"Total rows: {len(df_merged)}")
    print(f"Columns: {list(df_merged.columns)}")

    # Show sample
    print(f"\nSample merged data (first ticker with fundamentals):")
    # Find first ticker that has fundamental data
    for ticker in df_merged['ticker'].unique():
        ticker_data = df_merged[df_merged['ticker'] == ticker]
        if fund_vars and ticker_data[fund_vars[0]].notna().any():
            sample = ticker_data[ticker_data[fund_vars[0]].notna()].head(10)
            print(sample.to_string(index=False))
            break

    return df_merged

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    merge_monthly_fundamentals(sys.argv[1], sys.argv[2], sys.argv[3])
