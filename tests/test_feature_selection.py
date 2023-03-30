from functions import (
    merge_all_df,
    feature_selection,
    get_data_api,
    flatten_json,
)
from os import path
import pytest


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
