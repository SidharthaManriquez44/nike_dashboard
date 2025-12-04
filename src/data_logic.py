from datetime import datetime
import numpy as np
import pandas as pd

# ----------------------
# Simulate sample data
# ----------------------
def load_data(start_date=None, end_date=None):
    rng = pd.date_range(end=datetime.today(), periods=180, freq='D')
    df = pd.DataFrame({'date': rng})

    np.random.seed(42)

    base_revenue = 6_000_000
    seasonality = 1 + 0.15 * np.sin(np.linspace(0, 6.28 * 3, len(rng)))
    noise = np.random.normal(0, 0.04, len(rng))
    df['revenue'] = (base_revenue * seasonality * (1 + noise)).round(0)

    df['sessions'] = (200000 * (1 + 0.6 * np.sin(np.linspace(0, 3.14, len(rng))))
                      + np.random.randint(-15000, 15000, len(rng))).astype(int)

    df['conversion_rate'] = (0.015 + 0.005 * np.cos(np.linspace(0, 6.28, len(rng)))
                             + np.random.normal(0, 0.0015, len(rng)))

    df['orders'] = (df['sessions'] * df['conversion_rate']).round().astype(int)

    df['aov'] = (90 + 20 * np.cos(np.linspace(0, 3.14, len(rng)))
                 + np.random.normal(0, 3, len(rng))).round(2)

    regions = ['Americas', 'EMEA', 'APAC']
    region_share = [0.55, 0.30, 0.15]

    df_regions = []
    for region, share in zip(regions, region_share):
        df_regions.append(pd.DataFrame({
            'date': rng,
            'region': region,
            'revenue': df['revenue'] * share * (1 + np.random.normal(0, 0.05, len(rng)))
        }))

    df_regions = pd.concat(df_regions, ignore_index=True)

    df['inventory_turnover'] = 6 + np.sin(np.linspace(0, 6.28, len(rng))) + np.random.normal(0, 0.2, len(rng))
    df['stockout_rate'] = 0.02 + 0.01 * np.cos(np.linspace(0, 6.28, len(rng))) + np.random.normal(0, 0.002, len(rng))

    df['nps'] = 45 + 10 * np.sin(np.linspace(0, 3.14, len(rng))) + np.random.normal(0, 3, len(rng))

    df['forecast'] = df['revenue'].shift(7).bfill() * (1 + np.random.normal(0, 0.03, len(rng)))
    df['mape'] = ((df['revenue'] - df['forecast']).abs() / df['revenue']).rolling(14).mean().fillna(0)

    data = {'daily': df, 'regions': df_regions}

    if start_date:
        for k in data:
            data[k] = data[k][data[k]['date'] >= pd.to_datetime(start_date)]

    if end_date:
        for k in data:
            data[k] = data[k][data[k]['date'] <= pd.to_datetime(end_date)]

    return data

# ----------------------
# Auxiliary functions
# ----------------------
def compute_overview_metrics(df):
    revenue = float(df['revenue'].sum())
    yoy = ((df['revenue'].iloc[-1] - df['revenue'].iloc[0]) /
           max(df['revenue'].iloc[0], 1)) * 100

    return {
        'revenue': revenue,
        'yoy_growth': round(yoy, 2),
        'digital_share': 62.0,
        'clv': 180.0,
        'nps': round(float(df['nps'].iloc[-1]), 1),
        'inventory_turn': round(float(df['inventory_turnover'].mean()), 2),
    }
