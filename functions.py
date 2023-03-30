import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectKBest, f_regression

plt.rcParams["font.family"] = "Helvetica"


STATION_ID = "GHCND:USW00014739"
DATASET_ID = "GSOM"
START_DATE = "2013-04-01"
END_DATE = "2022-12-31"
LIMIT = "120"

WEATHER_TITLES = {
    "TAVG": ("Average Temperature", "Farenheit °"),
    "PRCP": ("Total Precipitation", "in"),
    "AWND": ("Average Wind Speed", "mph"),
}

SEASONS = {
    "Winter": ("12", "01", "02"),
    "Spring": ("03", "04", "05"),
    "Summer": ("06", "07", "08"),
    "Fall": ("09", "10", "11"),
}


def get_data_api(datatype_id):
    """
    Calls the Weather API to receive data of a desired datatype and stores
    into a .json file in the data folder.

    Args:
        datatype_id: a string that specifies the datatype ID parameter in
        the API function call.
    Returns:
        Nothing.
    """
    url = (
        f"https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid={DATASET_ID}"
        + f"&stationid={STATION_ID}&units=standard&startdate={START_DATE}"
        + f"&enddate={END_DATE}&limit={LIMIT}&datatypeid={datatype_id}"
    )

    with open("API_KEY.txt", "r", encoding="utf-8") as file:
        token = file.read()

    response = requests.get(url, headers={"token": token})

    response_json = response.json()

    json_name = f"{datatype_id}.json"

    with open("./data/" + json_name, "w", encoding="utf-8") as file:
        json.dump(response_json, file, ensure_ascii=False, indent=4)


def flatten_json(json_name):
    """
    Flattens .json file into a pandas dataframe.

    Args:
        json_name: a string containing the name of the .json file.
    Returns:
        A pandas dataframe containing the information in the .json file.
    """
    with open("./data/" + json_name + ".json", encoding="utf-8") as file:
        data = json.loads(file.read())
    data_frame = pd.json_normalize(data, record_path=["results"])
    return data_frame


def join_dataframes(df_weather, df_util):
    """
    Joins the chosen weather information dataframe with the Olin utilities
    dataframe by columns, and merges based on the column "year-month".

    Args:
        df_weather: the dataframe containing a specified type of weather
        information.
        df_util: the dataframe containing the Olin utility information.
    Returns:
        A joined pandas dataframe with df_weather and df_util.
    """
    df_util["start_read_date"] = pd.to_datetime(df_util["start_read_date"])
    df_util["year-month"] = df_util["start_read_date"].dt.strftime("%Y-%m")
    df_weather["date"] = pd.to_datetime(df_weather["date"])
    df_weather["year-month"] = df_weather["date"].dt.strftime("%Y-%m")
    df_util_weather = pd.merge(left=df_util, right=df_weather, on="year-month")
    df_util_weather_clean = df_util_weather.drop(
        columns=[
            "station",
            "attributes",
            "start_read_date",
            "end_read_date",
            "date",
        ]
    )
    return df_util_weather_clean


def join_dataframes1(df_weather, df_util):
    """
    Joins the chosen weather information dataframe with the Olin utilities
    dataframe by columns, and merges based on the column "year-month".

    Args:
        df_weather: the dataframe containing a specified type of weather
        information.
        df_util: the dataframe containing the Olin utility information.
    Returns:
        A joined pandas dataframe with df_weather and df_util.
    """
    df_util["start_read_date"] = pd.to_datetime(df_util["start_read_date"])
    df_util["year-month"] = df_util["start_read_date"].dt.strftime("%Y-%m")
    df_weather["date"] = pd.to_datetime(df_weather["date"])
    df_weather["year-month"] = df_weather["date"].dt.strftime("%Y-%m")
    df_util_weather = pd.merge(left=df_util, right=df_weather, on="year-month")

    return df_util_weather


def plot_data(df_util_weather):
    """
    Plots the data from the given pandas dataframe against the total
    consumption in the Olin utilities spreadsheet.

    Args:
        df_util_weather: a pandas dataframe containing information about a
        specific weather pattern and the utility information.
    Returns:
        Nothing.
    """
    weather_title_loc = WEATHER_TITLES[df_util_weather["datatype"].iloc[0]]
    plt.style.use("ggplot")
    fig, ax1 = plt.subplots(figsize=(8, 8))
    ax2 = ax1.twinx()

    ax1.plot(
        df_util_weather["datetime"],
        df_util_weather["value"],
        marker=".",
        color="blue",
    )

    ax2.plot(
        df_util_weather["datetime"],
        df_util_weather["Total Cons. (kwh)"],
        marker=".",
        color="red",
    )

    ax1.set_xlabel("Date")
    ax1.set_ylabel(
        f"{weather_title_loc[0]} ({weather_title_loc[1]})",
        color="blue",
        fontsize=14,
    )
    ax1.tick_params(axis="y", labelcolor="blue")
    ax2.set_ylabel("Total Electricity Consumption (kWh)", color="red", fontsize=14)
    ax2.tick_params(axis="y", labelcolor="red")
    fig.suptitle(f"{weather_title_loc[0]} vs. Utilities", fontsize=20)
    fig.autofmt_xdate()
    plt.show()


def filter_season(season, df_util_weather):
    """
    Filters the joined utilities and weather dataframe to only include rows
    from a specific season.
    Args:
        season: a string representing the desired season.
    Returns:
        A dataframe containing the joint weather and utilities data only from
        the specified season.
    """
    df_season = df_util_weather[
        df_util_weather["datetime"].dt.strftime("%m").isin(SEASONS[season])
    ]
    return df_season


def tidy_data(utility_data):
    """
    Tidy the utility data excel file.

    The function processes the excel file and creates a dataframe that abides
    to the three principles of tidy data:
        1. Every column is a variable.
        2. Every row is an observation.
        3. Every cell is a single value.
    First, read the excel file to a create dataframes for each fiscal year from
    2013 to 2023 with the information. Filter any columns with empty cells and
    transpose the dataframes. Additionally, filter only columns that are
    relevant to the scope of the project. Change the column names to snakecase
    and concacenate the dataframes to create a single dataframe that contains
    all the fiscal years. Save the dataframe locally as a .csv file.

    Args:
        utility data: a string that represent the path to the excel sheet
        containing the utility data.
    Returns:
        Nothing.
    """

    # Read the excel sheet and store them as a list of dataframes
    df_electric_all = []
    excel_electricity = pd.ExcelFile(utility_data)
    for i in range(13, 24):
        df_electric = pd.read_excel(
            excel_electricity, f"FY{i}", header=None, usecols="C:O", nrows=44
        )
        df_electric_transpose = df_electric.T
        valid_cols_mask = df_electric_transpose.iloc[0, :].notnull()
        df_electric_select = df_electric_transpose.loc[:, valid_cols_mask]
        df_electric_all.append(df_electric_select)

    # Select relevant data (columns) for the scope of the project
    df_electric_filtered = []
    for i in range(0, 11):
        useful_cols = [
            "Start Read Date",
            "End Read Date",
            "Time of Peak Demand",
            "Total Cons. (kwh)",
            "Total Monthly Electricity Cost",
        ]
        index_useful = df_electric_all[i].iloc[0, :].isin(useful_cols)
        df_electric_filtered.append(df_electric_all[i].loc[:, index_useful])
        df_electric_filtered[i].columns = [
            "start_read_date",
            "end_read_date",
            "total_consumption",
            "time_of_peak_demand",
            "total_cost",
        ]
        df_electric_filtered[i] = df_electric_filtered[i].iloc[1:, :]

    # Concatenating dataframes into a single long dataframe
    df_electric_long = pd.concat(df_electric_filtered, ignore_index=True)

    # Removing rows with NaN's
    df_electric_long.dropna(axis=0, inplace=True)

    # Save dataframe locally as a .csv file
    df_electric_long.to_csv("data/electricity_FY13_23.csv", index=False)


def merge_all_df(list_df_weather):
    """
    Merge all dataframes containing climate data and utility data.

    The function joins the climate dataframes by their `date` and uses the
    `join_dataframes` function to merge the utility dataframe with the merged
    climate dataframe. Additionally, the function wrangles the time and date
    columns into floats in order to utilize them in statistical tests.

    Args:
        list_df_weather: a list of climate pandas dataframes to be merged with
        the utility dataframe.
    Returns:
        df_all_data: a pandas dataframe that contains all the information from
        the utility dataset as well as the climate data.
    """
    col_names = ["date"]
    df_merge = list_df_weather[0]
    for df in list_df_weather[1:]:
        # Merge all the weather data together into a single dataframe
        df_merge = pd.merge(left=df_merge, right=df, on="date")

        # Keep only useful data
        df_filtered = df_merge.filter(regex="date|value|[A-Z]{4}", axis=1)

        # Set column name to the datatype (ex. TAVG)
        col_names = col_names + df_merge.filter(regex="datatype").iloc[0, :].tolist()
        df_filtered.columns = col_names
        df_merge = df_filtered

    # Merge another dataframe

    # Join the utility data and the weather data
    df_util = pd.read_csv("./data/electricity_FY13_23.csv")
    df_all_data = join_dataframes1(df_filtered, df_util)

    # Drop unnecessary columns
    df_all_data = df_all_data.drop(columns=["start_read_date", "end_read_date", "date"])

    # Convert time information to numerical values
    df_all_data["time_of_peak_demand"] = (
        pd.to_datetime(df_all_data["time_of_peak_demand"]).dt.hour
        + pd.to_datetime(df_all_data["time_of_peak_demand"]).dt.minute / 60
    )
    df_all_data["month"] = pd.to_datetime(df_all_data["year-month"]).dt.month

    return df_all_data


def test_features(features, target):
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

    fig, ax = plt.subplots()
    ax.barh(ylabels, df_results["F-Score"])
    ax.set_ylabel("Features")
    ax.set_xlabel("F-Score")
    ax.set_title("F-Score of Features for \nTotal Monthly Electricity Consumption")
    plt.show()
