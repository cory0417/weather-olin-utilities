from plotting import df_avg_temp, df_total_precp, df_util
import pandas as pd
import functions
from matplotlib import pyplot as plt


## join dataframes
df_joined = functions.join_dataframes(df_avg_temp, df_util)

## pulling useful columns
df_cons_temp = pd.DataFrame(
    [df_joined["year-month"], df_joined["Total Cons. (kwh)"], df_joined["value"]]
).transpose()

## Plot total consumption and average monthly temperature

# create a figure and axes objects
fig, ax = plt.subplots()

# plot the data on the axes object
ax.scatter(
    df_cons_temp["value"],
    df_cons_temp["Total Cons. (kwh)"],
)

# set the x and y labels
ax.set_xlabel("Temperature (F)")
ax.set_ylabel("Total Monthly Electricity Consumption (kWh)")

# set the plot title
ax.set_title(
    "Total Monthly Electricity Consumption vs \n Monthly Average Temperature of Boston FY13-23"
)

## calculating the spearman correlation coefficient

spearman_corr = df_cons_temp["value"].corr(
    df_cons_temp["Total Cons. (kwh)"], method="spearman"
)

plt.annotate(f"Spearman r = {spearman_corr:.2f}", (0.1, 0.9), xycoords="axes fraction")


# display the plot
plt.show()
