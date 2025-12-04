import pandas as pd
from src.data_logic import load_data
from datetime import datetime, timedelta

def test_load_data_default():
    data = load_data()

    # It must return a dictionary with 2 DataFrames
    assert isinstance(data, dict)
    assert "daily" in data
    assert "regions" in data
    assert isinstance(data["daily"], pd.DataFrame)
    assert isinstance(data["regions"], pd.DataFrame)

def test_load_data_date_filter():
    start = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
    end = datetime.today().strftime('%Y-%m-%d')

    data = load_data(start_date=start, end_date=end)
    df = data["daily"]

    assert df["date"].min() >= pd.to_datetime(start)
    assert df["date"].max() <= pd.to_datetime(end)

def test_load_data_regions_relation():
    data = load_data()
    df_daily = data["daily"]
    df_regions = data["regions"]

    # For each date, there must be 3 regions
    unique_dates = df_daily["date"].nunique()
    assert df_regions["date"].nunique() == unique_dates
