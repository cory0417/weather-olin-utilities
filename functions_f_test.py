"""
File containing helper functions for conducting the F-Test statistical analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectKBest, f_regression

plt.rcParams["font.family"] = "Helvetica"


def feature_selection(features, target):
    """
    Compute the F-scores and p-values of `features` for `target`.

    Create an instance of `SelectKBest` from sklearn module using
    `f_regression` as a parameter. Fit the features to the target and retrieve
    the f-scores and p-values. Return them with the features as a pandas
    dataframe.

    Args:
        features: a pandas dataframe that represents each feature as its
        column.
        target: a pandas dataframe of a single column that represents the
        target variable.
    Returns:
        df_results: a pandas dataframe that contains the f-score and p-value
        for each feature.
    """
    # Create an instance of SelectKBest using the f_regression method
    selector_k_best = SelectKBest(score_func=f_regression, k="all")
    selector_k_best.fit_transform(features, target)
    df_results = pd.DataFrame(
        {
            "Feature": features.columns,
            "F-Score": selector_k_best.scores_,
            "p-value": selector_k_best.pvalues_,
        }
    )
    df_results = df_results.sort_values("F-Score", ascending=False)

    return df_results


def plot_f_test(df_results):
    """
    Displays a horizontal bar plot of the f-scores with all features.

    Args:
        df_results: a pandas dataframe of the results of the ANOVA F-test using
        the `f_regression` method in sklearn module.
    Returns:
        Nothing.
    """
    df_results = df_results.sort_values("F-Score", ascending=True)
    ylabels = [
        "Monthly Total\n Precipitation",
        "Month of\n Year",
        "Time of\n Peak Demand",
        "Monthly Average\n Wind Speed",
        "Monthly Average\n Temperature",
        "Total Monthly\n Electricity Cost",
    ]

    _, ax1 = plt.subplots()
    ax1.barh(ylabels, df_results["F-Score"])
    ax1.set_ylabel("Features")
    ax1.set_xlabel("F-Score")
    ax1.set_title(
        "F-Score of Features for \nTotal Monthly Electricity Consumption"
    )
    plt.show()
