import functions
import pandas as pd

df_avg_temp_old = functions.flatten_json("TAVG.json")
df_avg_temp = df_avg_temp_old.loc[
    (df_avg_temp_old["date"] >= "2013-04-01")
    & (df_avg_temp_old["date"] <= "2022-11-01")
]

df_total_precp_old = functions.flatten_json("PRCP.json")
df_total_precp = df_total_precp_old.loc[
    (df_total_precp_old["date"] >= "2013-04-01")
    & (df_total_precp_old["date"] <= "2022-11-01")
]

# functions.plot_data(df_total_monthly_precp)

df_util = pd.read_csv("./data/electricity_FY13_23.csv")
# print(df_util.head())
# functions.plot_data(df_avg_monthly_temp, df_util)
df_avg_temp["datetime"] = pd.to_datetime(df_avg_temp["date"])
df_avg_temp["year-month"] = df_avg_temp["datetime"].dt.strftime("%Y-%m")
print(df_avg_temp)

# functions.join_dataframes(df_avg_monthly_temp, df_util)
