import functions
import pandas as pd

df_avg_temp = functions.flatten_json("TAVG")
df_total_precp = functions.flatten_json("PRCP")

df_util = pd.read_csv("./data/electricity_FY13_23.csv")
print(functions.join_dataframes(df_avg_temp, df_util))
