"""
File to run pytest unit tests on different helper functions in
functions_f_test.py
"""

import importlib.util
from os import path
import pytest

spec = importlib.util.spec_from_file_location(
    "function", "./functions_manage_data.py"
)
func_manage_data = importlib.util.module_from_spec(spec)
spec.loader.exec_module(func_manage_data)

spec = importlib.util.spec_from_file_location(
    "function", "./functions_f_test.py"
)
func_f_test = importlib.util.module_from_spec(spec)
spec.loader.exec_module(func_f_test)

DATATYPES = ["TAVG", "PRCP", "AWND"]

@pytest.fixture(scope="session")
def input_results():
    """
    Fixture to return a pandas dataframe of results after F-test.

    Args:
        Nothing.
    Returns:
        df_results: A pandas dataframe that represent the results of the F-test
        with features, F-score, p-value as its columns.
    """
    for datatype in DATATYPES:
        if path.isfile(f"data/{datatype}.json"):
            pass
        else:
            func_manage_data.get_data_api(datatype)

    df_avg_temp = func_manage_data.flatten_json("TAVG")
    df_total_prcp = func_manage_data.flatten_json("PRCP")
    df_avg_wind = func_manage_data.flatten_json("AWND")

    df_all_data = func_manage_data.merge_all_df(
        [df_avg_temp, df_avg_wind, df_total_prcp]
    )
    features = df_all_data.drop(columns=["total_consumption", "year-month"])
    target = df_all_data["total_consumption"]
    df_results = func_f_test.feature_selection(features, target)
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
