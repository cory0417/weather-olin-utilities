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

    with open(json_name, "w", encoding="utf-8") as f:
        json.dump(response_json, f, ensure_ascii=False, indent=4)

    with open(json_name, encoding="utf-8") as f:
        d = json.loads(f.read())

    # Flatten data
    df = pd.json_normalize(d, record_path=["results"])
    return df


def plot_data(df):
    """
    Plots the data from the given pandas dataframe.

    Args:
        df: a pandas dataframe containing information about a specific weather
        pattern.
    Returns:
        Nothing.
    """
    df["datetime"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
    plt.plot(df["datetime"], df["value"])
    plt.show()
