"""
File containing helper functions for plotting data.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.rcParams["font.family"] = "Helvetica"

WEATHER_TITLES = {
    "TAVG": ("Average Temperature", "Farenheit °", "orange"),
    "PRCP": ("Total Precipitation", "in", "dodgerblue"),
    "AWND": ("Average Wind Speed", "mph", "orchid"),
}


def plot_weather_util(df_util_weather, ax1):
    """
    Plots the data from the given pandas dataframe against the total
    consumption in the Olin utilities spreadsheet with two different axes.

    Args:
        df_util_weather: a pandas dataframe containing information about a
        specific weather pattern and the utility information.
        ax1: the first axes in the plot-- an already created subplot passed in
        from the outside where the plotting will occur.
    Returns:
        Nothing.
    """
    weather_title_loc = WEATHER_TITLES[df_util_weather["datatype"].iloc[0]]
    # make a twin axes of inputted subplot
    ax2 = ax1.twinx()

    # plot weather data on axes 1
    ax1.plot(
        df_util_weather["date"],
        df_util_weather["value"],
        color=weather_title_loc[2],
        label=weather_title_loc[0],
    )

    # plot util data on axes 2
    ax2.plot(
        df_util_weather["date"],
        df_util_weather["total_consumption"],
        color="seagreen",
        label="Total Cons.",
    )

    ax1.set_xlabel("Date", fontsize=14)
    ax1.set_ylabel(
        f"{weather_title_loc[0]} ({weather_title_loc[1]})",
        color="black",
        fontsize=14,
    )
    ax1.tick_params(axis="y", labelcolor="black")
    ax2.set_ylabel(
        "\nTotal Electricity Consumption (kWh)", color="black", fontsize=14
    )
    ax2.tick_params(axis="y", labelcolor="black")
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    # format dates on x-axis
    ax1.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 13)))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))


def plot_weather_util_corr(df_util_weather, subplot):
    """
    Plots the weather datatype against the total consumption in Olin
    electricity, with consumption on the x-axis and the weathertype
    on the y-axis. Includes a calculated linear trendline.

    Args:
        df_util_weather: a pandas dataframe containing information about a
        specific weather pattern and the utility information.
        subplot: an already-created subplot where the plotting will occur.
    Returns:
        Nothing.
    """
    weather_title_loc = WEATHER_TITLES[df_util_weather["datatype"].iloc[0]]
    # plot consumption data against weather data as scatter plot
    weather_data = df_util_weather["value"]
    consumption_data = df_util_weather["total_consumption"].astype(float)
    subplot.scatter(weather_data, consumption_data, color=weather_title_loc[2])
    subplot.set_xlabel(
        f"{weather_title_loc[0]} ({weather_title_loc[1]})", fontsize=14
    )

    # calculate line of best fit
    poly_fit = np.polyfit(weather_data, consumption_data, 1)
    equation_fit = np.poly1d(poly_fit)
    subplot.plot(
        weather_data,
        equation_fit(weather_data),
        color="red",
        label="Best Fit Line",
    )
    subplot.legend(loc="upper left")


def plot_weather_util_2_plots(df_util_weather):
    """
    Plots two subplots of the weather datatype against consumption with
    the first being both on the same axes and the second being consumption on
    the x-axis and weather data on y-axis.

    Args:
        df_util_weather: a pandas dataframe containing information about a
        specific weather pattern and the utility information.
    Returns:
        Nothing.
    """
    weather_title_loc = WEATHER_TITLES[df_util_weather["datatype"].iloc[0]]
    # create figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # plot same-axes plot on first subplot
    plot_weather_util(df_util_weather, ax1)

    # plot x-y axis plot on second subplot
    plot_weather_util_corr(df_util_weather, ax2)

    # subplot formatting
    fig.tight_layout(pad=5)
    plt.subplots_adjust(wspace=0.5)
    fig.suptitle(
        f"{weather_title_loc[0]} vs. Total Electricity Consumption", fontsize=20
    )
    plt.show()
