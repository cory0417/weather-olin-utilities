import pandas as pd
import matplotlib.pyplot as plt
import functions

df_avg_temp = functions.flatten_json("TAVG")
df_total_precp = functions.flatten_json("PRCP")
df_avg_wind_spd = functions.flatten_json("AWND")

df_util = pd.read_csv("./data/electricity_FY13_23.csv")

df_util_tavg = functions.join_dataframes(df_avg_temp, df_util)
df_util_prcp = functions.join_dataframes(df_avg_temp, df_util)

seasons = ["Winter", "Spring", "Summer", "Fall"]

season_dfs = []
for season in seasons:
    df = functions.filter_season(season, df_util_tavg)
    season_dfs.append(df.reset_index())

data = []
print(data)
for df in season_dfs:
    data.append(df["Total Cons. (kwh)"])

plt.boxplot(data, labels=seasons)
plt.ylabel("Total Energy Consumption (kwh)")
plt.title("Total Energy Consumption in each Season (kwh)")
plt.show()
