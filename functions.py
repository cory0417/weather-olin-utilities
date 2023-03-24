import json
import requests
import pandas as pd
import matplotlib.pyplot as plt

STATION_ID = "GHCND:USW00014739"
DATASET_ID = "GSOM"
START_DATE = "2013-01-01"
END_DATE = "2022-12-31"
LIMIT = "120"


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
    df_util["date"] = pd.to_datetime(df_util["Start Read Date"])
    df_util["year-month"] = df_util["date"].dt.strftime("%Y-%m")
    df_weather["datetime"] = pd.to_datetime(df_weather["date"])
    df_weather["year-month"] = df_weather["datetime"].dt.strftime("%Y-%m")
    df_util_weather = pd.merge(left=df_util, right=df_weather, on="year-month")
    return df_util_weather


def plot_data(df_weather, df_util):
    """
    Plots the data from the given pandas dataframe.

    Args:
        df: a pandas dataframe containing information about a specific weather
        pattern.
    Returns:
        Nothing.
    """
    df_weather["datetime"] = pd.to_datetime(
        df_weather["date"], format="%Y-%m-%d", errors="coerce"
    )
    fig, ax1 = plt.subplots(figsize=(8, 8))
    ax2 = ax1.twinx()

    plt.plot(df_weather["datetime"], df_weather["value"])
    plt.plot(df_weather["datetime"], df_util["Time of Peak Demand"])
    plt.show()
