import pandas as pd
from src.data_logic import compute_overview_metrics

def test_compute_overview_metrics_keys():
    df = pd.DataFrame({
        "date": pd.date_range("2024-01-01", periods=10, freq="D"),
        "revenue": [100,120,140,160,180,200,210,220,240,250],
        "nps": [40]*10,
        "inventory_turnover": [6]*10
    })

    results = compute_overview_metrics(df)

    expected_keys = {
        "revenue", "yoy_growth", "digital_share",
        "clv", "nps", "inventory_turn"
    }

    assert set(results.keys()) == expected_keys

def test_compute_overview_metrics_values():
    df = pd.DataFrame({
        "date": pd.date_range("2024-01-01", periods=2),
        "revenue": [100, 200],
        "nps": [50, 55],
        "inventory_turnover": [6, 7]
    })

    results = compute_overview_metrics(df)

    # Revenue total
    assert results["revenue"] == 300

    # Grow (200 - 100) / 100 = 100%
    assert results["yoy_growth"] == 100.0

    # NPS last value
    assert results["nps"] == 55

    # Turnover average
    assert results["inventory_turn"] == 6.5
