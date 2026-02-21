"""
Fetch monthly end-of-month data from Rice Data Portal.
Automatically includes: ticker, month, date, close, return, momentum, lag_month,
industry, sector, marketcap, size (based on marketcap percentiles).

IMPORTANT: Defaults to ALL stocks (including delisted) to avoid survivorship bias.

Usage:
  python rice_monthly_returns.py START_DATE OUTPUT_FILE
  python rice_monthly_returns.py TICKERS START_DATE OUTPUT_FILE

Examples:
  python rice_monthly_returns.py 2020-01-01 returns.parquet  # ALL stocks
  python rice_monthly_returns.py AAPL,MSFT 2020-01-01 returns.parquet  # Specific tickers
"""
import sys
import requests
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
from datetime import datetime

def fetch_monthly_returns(start_date, output_file, tickers=None):
    """Fetch end-of-month prices and calculate returns and momentum.

    Args:
        start_date: Start date in YYYY-MM-DD format
        output_file: Output filename (.parquet, .xlsx, or .csv)
        tickers: Optional comma-separated list of tickers. If None, fetches ALL stocks.
    """
    # Load environment
    load_dotenv()
    ACCESS_TOKEN = os.getenv('RICE_ACCESS_TOKEN')
    if not ACCESS_TOKEN:
        raise ValueError("RICE_ACCESS_TOKEN not found in .env file")

    API_URL = "https://data-portal.rice-business.org/api/query"

    # Parse inputs - default to ALL tickers if none specified
    if tickers is None:
        ticker_filter = ""
        print(f"Fetching monthly data for ALL stocks from {start_date}...")
        print(f"IMPORTANT: Including delisted stocks to avoid survivorship bias")
    else:
        ticker_list = [t.strip() for t in tickers.split(',')]
        ticker_str = "', '".join(ticker_list)
        ticker_filter = f"AND a.ticker IN ('{ticker_str}')"
        print(f"Fetching monthly data for {len(ticker_list)} specific tickers from {start_date}...")

    start_year = int(start_date[:4])
    current_year = datetime.now().year

    print(f"Automatic variables: ticker, month, date, close, return, momentum, lag_month,")
    print(f"                     industry, sector, marketcap, size")

    # First, fetch TICKERS data (one-time)
    print("Fetching ticker metadata (industry, sector)...")
    sql_tickers = "SELECT ticker, sector, industry FROM tickers"

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"},
        json={"query": sql_tickers},
        timeout=60
    )

    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch TICKERS data: {response.status_code}")

    tickers_data = response.json()
    if 'error' in tickers_data:
        raise RuntimeError(f"TICKERS query failed: {tickers_data['error']}")

    df_tickers = pd.DataFrame(tickers_data['data'])
    df_tickers = df_tickers[tickers_data['columns']]
    print(f"  Retrieved {len(df_tickers)} ticker records")

    # Now fetch SEP and DAILY data year-by-year and merge
    all_data = []
    for year in range(start_year, current_year + 1):
        print(f"\nFetching data for {year}...")

        # Fetch end-of-month prices from SEP
        sql_sep = f"""
        WITH month_ends AS (
          SELECT a.ticker, a.date::DATE as date, a.close, a.closeadj,
                 ROW_NUMBER() OVER (
                   PARTITION BY a.ticker, DATE_TRUNC('month', a.date::DATE)
                   ORDER BY a.date::DATE DESC
                 ) as rn
          FROM sep a
          WHERE a.date::DATE >= '{year}-01-01'
            AND a.date::DATE < '{year + 1}-01-01'
            {ticker_filter}
        )
        SELECT ticker, CAST(date AS VARCHAR) as date, close, closeadj
        FROM month_ends
        WHERE rn = 1
        ORDER BY ticker, date
        """

        response_sep = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"},
            json={"query": sql_sep},
            timeout=120
        )

        if response_sep.status_code != 200:
            raise RuntimeError(f"SEP query failed for {year}: {response_sep.status_code}")

        data_sep = response_sep.json()
        if 'error' in data_sep:
            raise RuntimeError(f"SEP query failed for {year}: {data_sep['error']}")

        if not data_sep.get('data'):
            print(f"  No SEP data for {year}")
            continue

        df_sep = pd.DataFrame(data_sep['data'])
        df_sep = df_sep[data_sep['columns']]
        print(f"  Retrieved {len(df_sep)} month-end prices from SEP")

        # Fetch end-of-month marketcap from DAILY
        sql_daily = f"""
        WITH month_ends AS (
          SELECT d.ticker, d.date::DATE as date, d.marketcap,
                 ROW_NUMBER() OVER (
                   PARTITION BY d.ticker, DATE_TRUNC('month', d.date::DATE)
                   ORDER BY d.date::DATE DESC
                 ) as rn
          FROM daily d
          WHERE d.date::DATE >= '{year}-01-01'
            AND d.date::DATE < '{year + 1}-01-01'
            {ticker_filter}
        )
        SELECT ticker, CAST(date AS VARCHAR) as date, marketcap
        FROM month_ends
        WHERE rn = 1
        ORDER BY ticker, date
        """

        response_daily = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"},
            json={"query": sql_daily},
            timeout=120
        )

        if response_daily.status_code != 200:
            raise RuntimeError(f"DAILY query failed for {year}: {response_daily.status_code}")

        data_daily = response_daily.json()
        if 'error' in data_daily:
            raise RuntimeError(f"DAILY query failed for {year}: {data_daily['error']}")

        if data_daily.get('data'):
            df_daily = pd.DataFrame(data_daily['data'])
            df_daily = df_daily[data_daily['columns']]
            print(f"  Retrieved {len(df_daily)} month-end marketcap values from DAILY")

            # Merge SEP and DAILY on (ticker, date)
            df_year = pd.merge(df_sep, df_daily, on=['ticker', 'date'], how='left')
        else:
            print(f"  No DAILY data for {year}, continuing without marketcap")
            df_year = df_sep
            df_year['marketcap'] = None

        all_data.append(df_year)
        print(f"  Year {year} complete: {len(df_year)} records")
    
    if not all_data:
        print("No data returned")
        return
    
    # Combine and process
    df = pd.concat(all_data, ignore_index=True)
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['date'] >= start_date].sort_values(['ticker', 'date']).reset_index(drop=True)

    # Merge with TICKERS data to add industry and sector
    print("Merging with ticker metadata (industry, sector)...")
    df = pd.merge(df, df_tickers, on='ticker', how='left')
    print(f"  Merge complete: {len(df)} total records")

    # Add month label
    df['month'] = df['date'].dt.to_period('M').astype(str)

    # CRITICAL: Calculate returns and momentum by ticker to avoid mixing data across stocks
    print("\nCalculating monthly metrics (return, momentum, lag_month)...")

    # 1. Monthly return: (closeadj / closeadj.shift(1)) - 1
    df['return'] = df.groupby('ticker')['closeadj'].pct_change().round(4)

    # 2. Momentum: 12-month return from 13 months ago to 2 months ago
    #    (closeadj.shift(2) / closeadj.shift(13)) - 1
    df['momentum'] = (
        df.groupby('ticker')['closeadj'].shift(2) /
        df.groupby('ticker')['closeadj'].shift(13) - 1
    ).round(4)

    # 3. Lag month: Prior month's return
    df['lag_month'] = df.groupby('ticker')['return'].shift(1).round(4)

    # CRITICAL: Shift marketcap by 1 month (by ticker) to avoid look-ahead bias
    # Marketcap for a given month should be the marketcap at the end of the prior month
    print("Shifting marketcap to represent prior month's value...")
    df['marketcap'] = df.groupby('ticker')['marketcap'].shift(1)

    # Calculate size categories based on marketcap percentiles for each month
    # Size is based on prior month's marketcap (already shifted above)
    print("Calculating size categories based on prior month's marketcap percentiles...")

    # Vectorized approach: calculate percentile rank within each month
    df['percentile'] = df.groupby('month')['marketcap'].rank(pct=True, method='average') * 100

    # Assign size categories based on percentile (vectorized)
    df['size'] = pd.cut(
        df['percentile'],
        bins=[0, 3.34, 18.83, 51.46, 78.60, 98.53, 100],
        labels=['Nano-Cap', 'Micro-Cap', 'Small-Cap', 'Mid-Cap', 'Large-Cap', 'Mega-Cap'],
        include_lowest=True
    )

    # Convert to string and handle NaN marketcap
    df['size'] = df['size'].astype(str)
    df.loc[df['marketcap'].isna(), 'size'] = None

    # Drop helper column
    df = df.drop(columns=['percentile'])

    # Final column order (DO NOT include closeadj in output)
    df = df[['ticker', 'month', 'date', 'close', 'return', 'momentum', 'lag_month',
             'industry', 'sector', 'marketcap', 'size']]
    
    # Save
    if output_file.endswith('.parquet'):
        df.to_parquet(output_file, index=False)
    elif output_file.endswith('.xlsx'):
        df.to_excel(output_file, index=False)
    elif output_file.endswith('.csv'):
        df.to_csv(output_file, index=False)
    else:
        raise ValueError("Output file must end with .parquet, .xlsx, or .csv")
    
    print(f"\nSaved {len(df)} rows to {output_file}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    return df

if __name__ == '__main__':
    if len(sys.argv) == 3:
        # No tickers specified - fetch ALL stocks
        fetch_monthly_returns(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        # Specific tickers provided
        fetch_monthly_returns(sys.argv[2], sys.argv[3], tickers=sys.argv[1])
    else:
        print(__doc__)
        sys.exit(1)
