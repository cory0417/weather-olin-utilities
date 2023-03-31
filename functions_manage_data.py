"""
File containing helper functions that manage and format data retrieved from
the weather API and the Olin utility spreadsheet.
"""
import json
import requests
import pandas as pd
import numpy as np

STATION_ID = "GHCND:USW00014739"
DATASET_ID = "GSOM"
START_DATE = "2013-04-01"
END_DATE = "2022-12-31"
LIMIT = "120"

PATH_UTILITY = "data/electricity_FY13_23.csv"
PATH_UTILITY_JITTERED = "data/electricity_FY13_23_jittered.csv"

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
    return df_util_weather


def calc_weather_util_corr(df_util_weather):
    """
    Calculates Pearson's coefficient correlation value between the values
    of a certain weather datatype and the total monthly electricity
    consumption.

    Args:
        df_util_weather: a pandas dataframe containing information about a
        specific weather pattern and the utility information.
    Returns:
        A floating point number representing the correlation.
    """

    weather_data = df_util_weather["value"]
    consumption_data = df_util_weather["total_consumption"].astype(float)
    return np.corrcoef(weather_data, consumption_data)[0][1]


def filter_season(season, df_util_weather):
    """
    Filters the joined utilities and weather dataframe to only include rows
    from a specific season.
    Args:
        season: a string representing the desired season.
        df_util_weather: a pandas dataframe containing information about a
        specific weather pattern and the utility information.
    Returns:
        A dataframe containing the joint weather and utilities data only from
        the specified season.
    """
    df_season = df_util_weather[
        df_util_weather["date"].dt.strftime("%m").isin(SEASONS[season])
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
    for dataframe in list_df_weather[1:]:
        # Merge all the weather data together into a single dataframe
        df_merge = pd.merge(left=df_merge, right=dataframe, on="date")

        # Keep only useful data
        df_filtered = df_merge.filter(regex="date|value|[A-Z]{4}", axis=1)

        # Set column name to the datatype (ex. TAVG)
        col_names = (
            col_names + df_merge.filter(regex="datatype").iloc[0, :].tolist()
        )
        df_filtered.columns = col_names
        df_merge = df_filtered

    # Merge another dataframe

    # Join the utility data and the weather data
    try:
        df_util = pd.read_csv(PATH_UTILITY)
    except FileNotFoundError:
        df_util = pd.read_csv(PATH_UTILITY_JITTERED)

    df_all_data = join_dataframes(df_filtered, df_util)

    # Drop unnecessary columns
    df_all_data = df_all_data.drop(
        columns=["start_read_date", "end_read_date", "date"]
    )

    # Convert time information to numerical values
    df_all_data["time_of_peak_demand"] = (
        pd.to_datetime(df_all_data["time_of_peak_demand"]).dt.hour
        + pd.to_datetime(df_all_data["time_of_peak_demand"]).dt.minute / 60
    )
    df_all_data["month"] = pd.to_datetime(df_all_data["year-month"]).dt.month

    return df_all_data
