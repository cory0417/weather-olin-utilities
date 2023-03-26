from functions import flatten_json, plot_data, join_dataframes
import pandas as pd

df_avg_temp = flatten_json("TAVG")
df_total_precp = flatten_json("PRCP")
df_avg_wind = flatten_json("AWND")
df_util = pd.read_csv("./data/electricity_FY13_23.csv")
df_util_wind = join_dataframes(df_avg_wind, df_util)
df_util_temp = join_dataframes(df_avg_temp, df_util)

plot_data(df_util_temp)
