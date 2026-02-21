"""
Check which variables are precomputed using cached schema (minimal cost).

This script uses WHERE 1=2 queries to get column names without downloading data.
Results are cached for 30 days to minimize database costs.

Usage:
    python check_precomputed.py pb,roe,asset_growth,leverage
    python check_precomputed.py --refresh  # Force refresh cache
"""
import sys
import requests
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

CACHE_FILE = Path(__file__).parent / 'schema_cache.json'
CACHE_DURATION_DAYS = 30  # Refresh cache monthly

def get_cached_or_fetch_columns():
    """Get column lists from cache or fetch if expired."""

    # Check cache
    if CACHE_FILE.exists():
        cache = json.loads(CACHE_FILE.read_text())
        cache_date = datetime.fromisoformat(cache['timestamp'])

        if datetime.now() - cache_date < timedelta(days=CACHE_DURATION_DAYS):
            print(f"[OK] Using cached schema from {cache_date.date()}")
            return cache['daily_cols'], cache['sf1_cols']

    # Cache expired or doesn't exist - fetch with WHERE 1=2
    print("Fetching schema from database (WHERE 1=2 - no data downloaded)...")

    load_dotenv()
    ACCESS_TOKEN = os.getenv('RICE_ACCESS_TOKEN')
    if not ACCESS_TOKEN:
        raise ValueError("RICE_ACCESS_TOKEN not found in .env file")

    API_URL = "https://data-portal.rice-business.org/api/query"

    def get_columns(table):
        sql = f"SELECT * FROM {table} WHERE 1=2"
        response = requests.post(API_URL,
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"},
            json={"query": sql}, timeout=60)

        if response.status_code == 200:
            return response.json().get('columns', [])
        raise RuntimeError(f"Failed to fetch {table} schema: {response.status_code}")

    daily_cols = get_columns('DAILY')
    sf1_cols = get_columns('SF1')

    print(f"  DAILY: {len(daily_cols)} columns")
    print(f"  SF1:   {len(sf1_cols)} columns")

    # Save to cache
    cache = {
        'timestamp': datetime.now().isoformat(),
        'daily_cols': daily_cols,
        'sf1_cols': sf1_cols
    }
    CACHE_FILE.write_text(json.dumps(cache, indent=2))
    print(f"[OK] Schema cached (refreshes every {CACHE_DURATION_DAYS} days)")

    return daily_cols, sf1_cols


def check_variables(requested_vars):
    """Check which variables are precomputed."""
    daily_cols, sf1_cols = get_cached_or_fetch_columns()

    daily_set = set(daily_cols)
    sf1_set = set(sf1_cols)

    results = {'daily': [], 'sf1': [], 'calculate': []}

    for var in requested_vars:
        if var in daily_set:
            results['daily'].append(var)
        elif var in sf1_set:
            results['sf1'].append(var)
        else:
            results['calculate'].append(var)

    return results


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == '--refresh':
        if CACHE_FILE.exists():
            CACHE_FILE.unlink()
        get_cached_or_fetch_columns()
        print("\n[OK] Cache refreshed successfully!")
        sys.exit(0)

    vars = [v.strip() for v in sys.argv[1].split(',')]
    results = check_variables(vars)

    print("\n" + "="*70)
    print("PRECOMPUTED VARIABLE CHECK")
    print("="*70)

    if results['daily']:
        print("\n[DAILY] MUST fetch from DAILY and shift by 1 period:")
        for v in results['daily']:
            print(f"  - {v}")

    if results['sf1']:
        print("\n[SF1] MUST fetch from SF1 and shift by 1 period:")
        for v in results['sf1']:
            print(f"  - {v}")

    if results['calculate']:
        print("\n[CALCULATE] NOT in DAILY/SF1 (OK to calculate manually):")
        for v in results['calculate']:
            print(f"  - {v}")

    print("\n" + "="*70)
    print("REMEMBER: All variables from DAILY/SF1 MUST be shifted by 1 period!")
    print("="*70 + "\n")
