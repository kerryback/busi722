"""
Master list of ALL precomputed variables from Rice Data Portal with aliases.

CRITICAL: These variables should NEVER be manually calculated.
They must be fetched from DAILY or SF1 tables and shifted appropriately.
"""

# Variables from DAILY table (all should be shifted by 1 month/week)
DAILY_PRECOMPUTED = {
    'ev': ['ev', 'enterprise_value', 'enterprise value', 'enterprisevalue'],
    'evebit': ['evebit', 'ev/ebit', 'ev_ebit', 'enterprise_value_ebit'],
    'evebitda': ['evebitda', 'ev/ebitda', 'ev_ebitda', 'enterprise_value_ebitda'],
    'marketcap': ['marketcap', 'market_cap', 'market cap', 'market_capitalization', 'market capitalization'],
    'pb': ['pb', 'p/b', 'p_b', 'price_to_book', 'price to book', 'price-to-book', 'pricetobook', 'book_to_market_inv'],
    'pe': ['pe', 'p/e', 'p_e', 'price_to_earnings', 'price to earnings', 'price-to-earnings', 'pricetoearnings'],
    'ps': ['ps', 'p/s', 'p_s', 'price_to_sales', 'price to sales', 'price-to-sales', 'pricetosales'],
}

# Ratios and computed metrics from SF1 table (all should be shifted)
SF1_PRECOMPUTED_RATIOS = {
    # Profitability ratios
    'roa': ['roa', 'return_on_assets', 'return on assets', 'returnonassets'],
    'roe': ['roe', 'return_on_equity', 'return on equity', 'returnonequity'],
    'roic': ['roic', 'return_on_invested_capital', 'return on invested capital', 'returnoninvestedcapital'],
    'ros': ['ros', 'return_on_sales', 'return on sales', 'returnonsales'],

    # Margin ratios
    'ebitdamargin': ['ebitdamargin', 'ebitda_margin', 'ebitda margin'],
    'grossmargin': ['grossmargin', 'gross_margin', 'gross margin'],
    'netmargin': ['netmargin', 'net_margin', 'net margin', 'profit_margin', 'profit margin'],

    # Liquidity ratios
    'currentratio': ['currentratio', 'current_ratio', 'current ratio'],

    # Leverage ratios
    'de': ['de', 'd/e', 'd_e', 'debt_to_equity', 'debt to equity', 'debt-to-equity', 'debttoequity', 'debt_equity_ratio', 'leverage_ratio'],

    # Efficiency ratios
    'assetturnover': ['assetturnover', 'asset_turnover', 'asset turnover'],

    # Valuation ratios (from SF1)
    'pb': ['pb', 'p/b', 'p_b', 'price_to_book', 'price to book', 'price-to-book', 'pricetobook'],
    'pe': ['pe', 'p/e', 'p_e', 'price_to_earnings', 'price to earnings', 'price-to-earnings', 'pricetoearnings'],
    'pe1': ['pe1', 'forward_pe', 'forward p/e', 'forward_p/e'],
    'ps': ['ps', 'p/s', 'p_s', 'price_to_sales', 'price to sales', 'price-to-sales', 'pricetosales'],
    'ps1': ['ps1', 'forward_ps', 'forward p/s', 'forward_p/s'],

    # Other ratios
    'divyield': ['divyield', 'div_yield', 'dividend_yield', 'dividend yield'],
    'payoutratio': ['payoutratio', 'payout_ratio', 'payout ratio', 'dividend_payout_ratio'],

    # Per-share metrics (derived/computed)
    'bvps': ['bvps', 'book_value_per_share', 'book value per share'],
    'dps': ['dps', 'dividends_per_share', 'dividends per share'],
    'eps': ['eps', 'earnings_per_share', 'earnings per share'],
    'epsdil': ['epsdil', 'eps_diluted', 'diluted_eps', 'diluted earnings per share'],
    'epsusd': ['epsusd', 'eps_usd', 'earnings_per_share_usd'],
    'fcfps': ['fcfps', 'fcf_per_share', 'free_cash_flow_per_share', 'free cash flow per share'],
    'sps': ['sps', 'sales_per_share', 'sales per share', 'revenue_per_share'],
    'tbvps': ['tbvps', 'tangible_book_value_per_share', 'tangible book value per share'],
}


def normalize_variable_name(name):
    """Normalize variable name for comparison."""
    return name.lower().replace('_', '').replace('-', '').replace(' ', '').replace('/', '')


def build_alias_map():
    """Build a mapping from all aliases to canonical variable names."""
    alias_map = {}

    # Add DAILY variables
    for canonical, aliases in DAILY_PRECOMPUTED.items():
        for alias in aliases:
            normalized = normalize_variable_name(alias)
            alias_map[normalized] = ('daily', canonical)

    # Add SF1 variables
    for canonical, aliases in SF1_PRECOMPUTED_RATIOS.items():
        for alias in aliases:
            normalized = normalize_variable_name(alias)
            # Don't overwrite DAILY mappings (DAILY takes precedence)
            if normalized not in alias_map:
                alias_map[normalized] = ('sf1', canonical)

    return alias_map


# Build the alias map once
ALIAS_MAP = build_alias_map()


def validate_no_manual_calculation(variables_to_calculate):
    """
    Validate that we're not manually calculating any precomputed variables.
    Checks both exact names and common aliases/variations.

    Args:
        variables_to_calculate: List or set of variable names about to be calculated

    Raises:
        ValueError: If any variables are precomputed and should be fetched instead
    """
    conflicts = []

    for var in variables_to_calculate:
        normalized = normalize_variable_name(var)
        if normalized in ALIAS_MAP:
            source, canonical = ALIAS_MAP[normalized]
            conflicts.append((var, canonical, source))

    if conflicts:
        error_msg = [
            "\n" + "="*80,
            "ERROR: Attempting to manually calculate precomputed variables!",
            "="*80,
            "\nThe following variables are precomputed in DAILY/SF1 tables:",
        ]

        for requested, canonical, source in sorted(conflicts, key=lambda x: x[2]):
            if requested.lower() != canonical:
                error_msg.append(f"  - '{requested}' → {canonical} (from {source.upper()} table)")
            else:
                error_msg.append(f"  - {canonical} (from {source.upper()} table)")

        error_msg.extend([
            "\nYou MUST:",
            "1. Fetch these variables from their respective tables",
            "2. Shift them by 1 period (grouped by ticker) to avoid look-ahead bias",
            "3. DO NOT manually calculate them",
            "\nSee .claude/skills/monthly-analysis/SKILL.md for details.",
            "="*80
        ])

        raise ValueError('\n'.join(error_msg))


def get_canonical_name(variable_name):
    """
    Get the canonical database column name for a variable.

    Args:
        variable_name: Variable name (could be alias)

    Returns:
        tuple: (source, canonical_name) or (None, None) if not found
    """
    normalized = normalize_variable_name(variable_name)
    return ALIAS_MAP.get(normalized, (None, None))


def get_variables_to_fetch(requested_variables):
    """
    Determine which variables should be fetched from DAILY vs SF1.
    Handles aliases and returns canonical names.

    Args:
        requested_variables: List of variable names needed (can include aliases)

    Returns:
        dict: {'daily': [...], 'sf1': [...], 'calculate': [...]}
    """
    result = {
        'daily': set(),
        'sf1': set(),
        'calculate': []
    }

    for var in requested_variables:
        source, canonical = get_canonical_name(var)
        if source == 'daily':
            result['daily'].add(canonical)
        elif source == 'sf1':
            result['sf1'].add(canonical)
        else:
            result['calculate'].append(var)

    # Convert sets to sorted lists
    result['daily'] = sorted(result['daily'])
    result['sf1'] = sorted(result['sf1'])

    return result


if __name__ == '__main__':
    # Print summary
    print("="*80)
    print("PRECOMPUTED VARIABLES IN RICE DATA PORTAL")
    print("="*80)

    print(f"\nDAILY table ({len(DAILY_PRECOMPUTED)} variables):")
    for canonical, aliases in sorted(DAILY_PRECOMPUTED.items()):
        print(f"  {canonical:20s} - Aliases: {', '.join(aliases[:3])}")

    print(f"\nSF1 table ({len(SF1_PRECOMPUTED_RATIOS)} precomputed ratios):")
    for canonical, aliases in sorted(SF1_PRECOMPUTED_RATIOS.items()):
        print(f"  {canonical:20s} - Aliases: {', '.join(aliases[:3])}")

    print(f"\nTotal precomputed variables: {len(DAILY_PRECOMPUTED) + len(SF1_PRECOMPUTED_RATIOS)}")
    print(f"Total aliases tracked: {len(ALIAS_MAP)}")

    # Test examples
    print("\n" + "="*80)
    print("EXAMPLE LOOKUPS")
    print("="*80)
    test_names = ['price to book', 'market cap', 'return on equity', 'pb', 'roe', 'leverage']
    for name in test_names:
        source, canonical = get_canonical_name(name)
        if source:
            print(f"  '{name}' → {canonical} (from {source.upper()} table)")
        else:
            print(f"  '{name}' → Not found (OK to calculate)")

    print("\n" + "="*80)
    print("NEVER MANUALLY CALCULATE THESE - FETCH AND SHIFT THEM INSTEAD!")
    print("="*80)
