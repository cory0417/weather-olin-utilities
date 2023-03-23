import functions

df_avg_monthly_temp = functions.get_data_api("TAVG")
print(df_avg_monthly_temp)
df_total_monthly_precp = functions.get_data_api("PRCP")
print(df_total_monthly_precp)
