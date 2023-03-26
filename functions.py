import json
import requests
import pandas as pd
import matplotlib.pyplot as plt

STATION_ID = "GHCND:USW00014739"
DATASET_ID = "GSOM"
START_DATE = "2013-01-01"
END_DATE = "2022-12-31"
LIMIT = "120"

WEATHER_TITLES = {
    "TAVG": ("Average Temperature", "Farenheit °"),
    "PRCP": ("Total Precipitation", "in"),
}

SEASONS = {
    "winter": ("12", "01", "02"),
    "spring": ("03", "04", "05"),
    "summer": ("06", "07", "08"),
    "fall": ("09", "10", "11"),
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
    df_util["date"] = pd.to_datetime(df_util["Start Read Date"])
    df_util["year-month"] = df_util["date"].dt.strftime("%Y-%m")
    df_weather["datetime"] = pd.to_datetime(df_weather["date"])
    df_weather["year-month"] = df_weather["datetime"].dt.strftime("%Y-%m")
    df_util_weather = pd.merge(left=df_util, right=df_weather, on="year-month")
    df_util_weather_clean = df_util_weather.drop(
        columns=[
            "station",
            "attributes",
            "Start Read Date",
            "End Read Date",
            "date_x",
            "date_y",
        ]
    )
    return df_util_weather_clean


def plot_data(df_util_weather):
    """
    Plots the data from the given pandas dataframe against the total
    consumption in the Olin utilities spreadsheet.

    Args:
        df_util_weather: a pandas dataframe containing information about a
        specific weather pattern.
    Returns:
        Nothing.
    """
    weather_title_loc = WEATHER_TITLES[df_util_weather["datatype"][0]]

    fig, ax1 = plt.subplots(figsize=(8, 8))
    ax2 = ax1.twinx()

    ax1.plot(df_util_weather["datetime"], df_util_weather["value"], color="blue", lw=1)

    ax2.plot(
        df_util_weather["datetime"],
        df_util_weather["Total Cons. (kwh)"],
        color="red",
        lw=1,
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
