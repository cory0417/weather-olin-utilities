import functions
import pandas as pd

df_avg_temp = functions.flatten_json("TAVG")
df_total_precp = functions.flatten_json("PRCP")

df_util = pd.read_csv("./data/electricity_FY13_23.csv")

df_util_tavg = functions.join_dataframes(df_avg_temp, df_util)
df_util_prcp = functions.join_dataframes(df_avg_temp, df_util)

df_winter = functions.filter_season("winter", df_util_tavg)
df_spring = functions.filter_season("spring", df_util_tavg)
df_summer = functions.filter_season("summer", df_util_tavg)
df_fall = functions.filter_season("fall", df_util_tavg)
