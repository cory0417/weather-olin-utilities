import json
import requests
import pandas as pd

# Build url
STATION_ID = "GHCND:USW00014739"
DATASET_ID = "GSOM"
START_DATE = "2013-01-01"
END_DATE = "2022-12-31"
DATA_TYPE = "TAVG"
LIMIT = "120"

url = (
    f"https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid={DATASET_ID}"
    + f"&stationid={STATION_ID}&units=standard&startdate={START_DATE}"
    + f"&enddate={END_DATE}&limit={LIMIT}&datatypeid={DATA_TYPE}"
)

with open("API_KEY.txt", "r", encoding="utf-8") as f:
    token = f.read()

response = requests.get(url, headers={"token": token})

response_json = response.json()

with open("avg_monthly_temp.json", "w", encoding="utf-8") as f:
    json.dump(response_json, f, ensure_ascii=False, indent=4)

with open("avg_monthly_temp.json", encoding="utf-8") as f:
    d = json.loads(f.read())

# Flatten data
df_avg_monthly_temp = pd.json_normalize(d, record_path=["results"])
print(df_avg_monthly_temp)
