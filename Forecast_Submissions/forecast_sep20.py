#%%
import numpy as np

filename =('https://raw.githubusercontent.com/HAS-Tools-Fall2022'                               
           '/Course-Materials22/main/data/verde_river_daily_flow_cfs.csv')

flows = np.loadtxt(
    filename,           # The location of the text file
    delimiter=',',      # character which splits data into groups
    usecols=1           # Just take column 1, which is the flows
)
print(flows)
len(flows)
# %%

flow_last_week = flows[23], flows[24], flows[25], flows[26], flows[27], flows[28], flows[-1]
print(flow_last_week)
last_week_change = flows[23]- flows[-1]
print(last_week_change)
# %%
week1_prediction = np.mean(flow_last_week) - (last_week_change/2)
print(week1_prediction)

week2_prediction = np.mean(flow_last_week) - last_week_change
print(week2_prediction)
# %%

# %%
