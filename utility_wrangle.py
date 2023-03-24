import pandas as pd
from matplotlib import pyplot as plt

df_electric_all = []
excel_electricity = pd.ExcelFile("data/FY23_Electric_Data_Campus_Houses_edited.xlsx")
for i in range(13, 24):
    df_electric = pd.read_excel(
        excel_electricity, f"FY{i}", header=None, usecols="C:O", nrows=44
    )
    df_electric_transpose = df_electric.T
    valid_cols_mask = df_electric_transpose.iloc[0, :].notnull()
    df_electric_select = df_electric_transpose.loc[:, valid_cols_mask]
    df_electric_all.append(df_electric_select)


# Select relevant data for the scope of the project

df_electric_filtered = []
for i in range(0, 11):
    useful_cols = [
        "Start Read Date",
        "End Read Date",
        "Time of Peak Demand",
        "Total Cons. (kwh)",
        "Total Monthly Electricity Cost",
    ]
    df_electric_filtered.append(
        df_electric_all[i].loc[:, df_electric_all[i].iloc[0, :].isin(useful_cols)]
    )
    df_electric_filtered[i].columns = [
        "Start Read Date",
        "End Read Date",
        "Total Cons. (kwh)",
        "Time of Peak Demand",
        "Total Monthly Electricity Cost",
    ]
    df_electric_filtered[i] = df_electric_filtered[i].iloc[1:, :]

# Concatenating dataframes into a single long dataframe
df_electric_long = pd.concat(df_electric_filtered, ignore_index=True)

# Removing rows with NaN's
df_electric_long.dropna(axis=0, inplace=True)

print(df_electric_long)

# Sample plot using the cleaned data

# create a figure and axes objects
fig, ax = plt.subplots()


# plot the data on the axes object
ax.plot(
    df_electric_long["Start Read Date"],
    df_electric_long["Total Monthly Electricity Cost"],
)

# set the x and y labels
ax.set_xlabel("Start Read Date")
ax.set_ylabel("Total Monthly Electricity Cost ($)")

# set the plot title
ax.set_title("Total Monthly Electricity Cost FY13-23")

# display the plot
plt.show()

# Save dataframe as a .csv file
df_electric_long.to_csv("data/electricity_FY13_23.csv", index=False)
