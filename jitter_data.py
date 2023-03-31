"""
Function file for scrambling the Olin Utility data so that there is data to
demonstrate on while keeping the Olin data secure.
"""

import pandas as pd
import numpy as np


def add_jitter(x_int, factor):
    """
    Add jitter to the value by adding a random value with a factor.

    Args:
        x: An integer value to be jittered.
        factor: An integer value that represents the factor in which the random
        value between -1 and +1 will be multiplied by and added to `x`.
    Returns:
        x_jittered: An integer that represents the value aftering jittering.
    """
    x_jittered = x_int + factor * np.random.normal(0, 1)
    return x_jittered


def jitter_utility_df(file_directory):
    """
    Apply jitter to the raw utility data and save it as a .csv file.

    Args:
        file_directory: A string that represents the file directory to the raw
        utility data.
    Returns:
        Nothing.
    """
    df_utility_raw = pd.read_csv(file_directory)

    # filter only sensitive data
    df_jittered = df_utility_raw.filter(
        items=[
            "total_consumption",
            "time_of_peak_demand",
            "total_cost",
        ]
    )

    # convert time of day into a float value
    df_jittered["time_of_peak_demand"] = df_jittered["time_of_peak_demand"] = (
        pd.to_datetime(df_jittered["time_of_peak_demand"]).dt.hour
        + pd.to_datetime(df_jittered["time_of_peak_demand"]).dt.minute / 60
    )

    # apply the jitter function to the dataframes with different factors
    # depending on their typical magnitude
    df_jittered["total_consumption"] = df_jittered["total_consumption"].apply(
        add_jitter, factor=5e4
    )
    df_jittered["total_cost"] = df_jittered["total_cost"].apply(
        add_jitter, factor=5e3
    )
    df_jittered["time_of_peak_demand"] = df_jittered[
        "time_of_peak_demand"
    ].apply(add_jitter, factor=1e0)

    # convert the time of peak demand to a time object
    df_jittered["hour"] = (df_jittered["time_of_peak_demand"] // 1).astype(int)
    df_jittered["minute"] = (
        df_jittered["time_of_peak_demand"] - df_jittered["hour"]
    ) * 60
    df_jittered["minute"] = df_jittered["minute"].astype(int)
    df_jittered["time_of_peak_demand"] = pd.to_datetime(
        df_jittered["hour"].astype(str)
        + ":"
        + df_jittered["minute"].astype(str),
        format="%H:%M",
    ).dt.time

    df_jittered = df_jittered.drop(columns=["hour", "minute"])

    # merge back with the data that was excluded from the jitter
    df_jittered = pd.merge(
        df_utility_raw.filter(items=["start_read_date", "end_read_date"]),
        df_jittered,
        left_index=True,
        right_index=True,
    )

    # save as a csv file locally
    df_jittered.to_csv("data/electricity_FY13_23_jittered.csv", index=False)
