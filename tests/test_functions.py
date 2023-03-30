"""
File to run pytest unit tests on different helper functions in functions.py
"""

from os import path
import pandas as pd
import pytest

from functions import (
    merge_all_df,
    feature_selection,
    get_data_api,
    flatten_json,
    filter_season,
    join_dataframes,
)


@pytest.fixture(scope="session")
def input_results():
    DATATYPES = ["TAVG", "PRCP", "AWND"]

    for datatype in DATATYPES:
        if path.isfile(f"data/{datatype}.json"):
            pass
        else:
            get_data_api(datatype)

    df_avg_temp = flatten_json("TAVG")
    df_total_prcp = flatten_json("PRCP")
    df_avg_wind = flatten_json("AWND")

    df_all_data = merge_all_df([df_avg_temp, df_avg_wind, df_total_prcp])
    features = df_all_data.drop(columns=["total_consumption", "year-month"])
    target = df_all_data["total_consumption"]
    df_results = feature_selection(features, target)
    print("test")
    print(df_results)
    return df_results


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
        get_data_api("TAVG")

    df_avg_temp = flatten_json("TAVG")
    df_util = pd.read_csv("./data/electricity_FY13_23.csv")
    df_util_temp = join_dataframes(df_avg_temp, df_util)
    return df_util_temp


def test_f_score(input_results):
    """
    Check that F-Scores are all positive values.

    Since the F-test should not be returning any negative f-score values, the
    values must all be a positive value.

    Args:
        df_results: A pandas dataframe that contains the results of the F-test
        with "F-Score" as one of its columns.
    """
    assert (input_results["F-Score"] >= 0).all()


def test_p_value(input_results):
    """
    Check that p-values are all positive values.

    Since p-values represent probabilities, the F-test should not be returning
    any negative p-values.

    Args:
        df_results: A pandas dataframe that contains the results of the F-test
        with "p-value" as one of its columns.
    """
    assert (input_results["p-value"] >= 0).all()


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
    """
    filtered_df = filter_season(season_name, create_df)
    assert all(
        pd.to_datetime(filtered_df["year-month"])
        .dt.strftime("%m")
        .isin(season_nums)
    )
