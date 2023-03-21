import pandas as pd
import matplotlib.pyplot as plt
from get_data import df_avg_monthly_temp

df_avg_monthly_temp["datetime"] = pd.to_datetime(
    df_avg_monthly_temp["date"], format="%Y-%m-%d", errors="coerce"
)

print(df_avg_monthly_temp.head(5))
plt.plot(df_avg_monthly_temp["datetime"], df_avg_monthly_temp["value"])
plt.show()
