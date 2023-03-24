import json
import requests
import pandas as pd
import matplotlib.pyplot as plt


def get_data_api(
    datatype_id,
    STATION_ID="GHCND:USW00014739",
    DATASET_ID="GSOM",
    START_DATE="2013-01-01",
    END_DATE="2022-12-31",
    LIMIT="120",
):
    """
    Calls the Weather API to receive data of a certain datatype.

    Args:
        datatype_id: a string that specifies the datatype ID parameter in
        the API function call.
        STATION_ID: a string set to the Boston Logan Airport weather station
        ID to use in the API function call.
        DATASET_ID: a string set to specifiy the dataset ID used in the API
        function call.
        START_DATE: a string set to the starting date to begin collecting data.
        END_DATE: a string set to the date where the collection of data ends.
        LIMIT: a string set to the maximum number of results in the response.
    Returns:
        A pandas dataframe containing all the information from the start
        date to the end date of the certain data type.
    """
    url = (
        f"https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid={DATASET_ID}"
        + f"&stationid={STATION_ID}&units=standard&startdate={START_DATE}"
        + f"&enddate={END_DATE}&limit={LIMIT}&datatypeid={datatype_id}"
    )

    with open("API_KEY.txt", "r", encoding="utf-8") as f:
        token = f.read()

    response = requests.get(url, headers={"token": token})

    response_json = response.json()

    json_name = f"{datatype_id}.json"

    with open("./data/" + json_name, "w", encoding="utf-8") as f:
        json.dump(response_json, f, ensure_ascii=False, indent=4)


def flatten_json(json_name):
    # Flatten data
    with open("./data/" + json_name, encoding="utf-8") as f:
        d = json.loads(f.read())
    df = pd.json_normalize(d, record_path=["results"])
    return df


def join_dataframes(df_weather, df_util):
    df_util["date"] = pd.to_datetime(df_util["Start Read Date"])
    df_util["year-month"] = df_util["date"].dt.strftime("%Y-%m")
    df_weather["datetime"] = pd.to_datetime(df_weather["date"])
    df_weather["year-month"] = df_weather["datetime"].dt.strftime("%Y-%m")
    print(df_weather)


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
