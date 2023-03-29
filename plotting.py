from functions import flatten_json
import pandas as pd

df_avg_temp = flatten_json("TAVG")
df_total_precp = flatten_json("PRCP")
df_avg_wind = flatten_json("AWND")
df_util = pd.read_csv("./data/electricity_FY13_23.csv")
