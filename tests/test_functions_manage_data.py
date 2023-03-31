"""
File to run pytest unit tests on different helper functions in
functions_manage_data.py
"""

from os import path
import importlib.util
import pandas as pd
import pytest

spec = importlib.util.spec_from_file_location(
    "function", "./functions_manage_data.py"
)
func_manage_data = importlib.util.module_from_spec(spec)
spec.loader.exec_module(func_manage_data)


@pytest.fixture(scope="session")
def create_df():
    """
    Creates a dataframe containing all weather and utility information
    of the TAVG datatype for testing purposes.

    Args:
        Nothing
    Returns:
        A pandas dataframe containing all weather and utility information
        about the TAVG datatype.
    """
    if path.isfile("data/TAVG.json"):
        pass
    else:
        func_manage_data.get_data_api("TAVG")

    df_avg_temp = func_manage_data.flatten_json("TAVG")
    df_util = pd.read_csv("./data/electricity_FY13_23.csv")
    df_util_temp = func_manage_data.join_dataframes(df_avg_temp, df_util)
    return df_util_temp


filter_season_cases = [
    ("Winter", ["12", "01", "02"]),
    ("Spring", ["03", "04", "05"]),
    ("Summer", ["06", "07", "08"]),
    ("Fall", ["09", "10", "11"]),
]


@pytest.mark.parametrize("season_name,season_nums", filter_season_cases)
def test_filter_season(season_name, season_nums, create_df):
    """
    Check that the returned dataframe actually filters out the right months
    for the given season.

    Args:
        season_name: the string name of the season
        season_nums: a list of string representations of each numerical month
        in each season
        create_df: the dataframe returned by create_df()-- a sample of a full
        dataframe containing all the weather and utility information
    """
    filtered_df = func_manage_data.filter_season(season_name, create_df)
    assert all(
        pd.to_datetime(filtered_df["year-month"])
        .dt.strftime("%m")
        .isin(season_nums)
    )
