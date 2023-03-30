from functions import merge_all_df, test_features
from plotting import df_avg_temp, df_avg_wind, df_total_precp

df_all_data = merge_all_df([df_avg_temp, df_avg_wind, df_total_precp])
features = df_all_data.drop(columns=["total_consumption", "year-month"])
target = df_all_data["total_consumption"]

df_results = test_features(features, target)


def test_f_score(df_results):
    """
    Check that F-Scores are all positive values.

    Since the F-test should not be returning any negative f-score values, the
    values must all be a positive value.

    Args:
        df_results: A pandas dataframe that contains the results of the F-test
        with "F-Score" as one of its columns.
    """
    assert (df_results["F-Score"] >= 0).all()


def test_p_value(df_results):
    """
    Check that p-values are all positive values.

    Since p-values represent probabilities, the F-test should not be returning
    any negative p-values.

    Args:
        df_results: A pandas dataframe that contains the results of the F-test
        with "p-value" as one of its columns.
    """
    assert (df_results["p-value"] >= 0).all()
