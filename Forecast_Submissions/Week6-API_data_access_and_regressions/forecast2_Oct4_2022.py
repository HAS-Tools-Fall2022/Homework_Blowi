#%%
import urllib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


# %%
def create_usgs_url(site_no, begin_date, end_date):
    return (
        f'https://waterdata.usgs.gov/nwis/dv?'
        f'cb_00060=on&format=rdb&referred_module=sw&'
        f'site_no={site_no}&'
        f'begin_date={begin_date}&'
        f'end_date={end_date}'
    )

def open_usgs_data(site, begin_date, end_date):
    url = create_usgs_url((site), begin_date, end_date)
    response = urllib.request.urlopen(url)
    df = pd.read_table(
        response,
        comment='#',
        skipfooter=1,
        delim_whitespace=True,
        names=['agency', 'site', 'date', 'streamflow', 'quality_flag'],
        index_col=2,
        parse_dates=True
    ).iloc[2:]

    # Now convert the streamflow data to floats and
    # the index to datetimes. When processing raw data
    # it's common to have to do some extra postprocessing
    df['streamflow'] = df['streamflow'].astype(np.float64)
    df.index = pd.DatetimeIndex(df.index)
    return df



# %%
# Step 1: Open up 30 years of daily data for the Verde River stream gauge
#         and put it into a pandas dataframe called `df`

#TODO: Your code here
site = '09506000'
begin_date = '1992-09-29'
end_date = '2022-09-29'
df = open_usgs_data(site, begin_date, end_date)
df['streamflow'].plot()
plt.semilogy()
plt.ylabel('Streamflow [cfs]')
plt.xlabel('')

# %%
# Step 2: Convert the daily data into weekly means in a new 
#         dataframe called `weekly_df`

#TODO: Your code here
weekly_df = df.resample('W').mean()

# %%

weekly_df.iloc

weekly_df1 = weekly_df.iloc[0:-1]
print(weekly_df1)

weekly_df2 = weekly_df.iloc[1:]
print(weekly_df2)

# %%
# Step 3: Create 2 variables, `x` and `y` where `x` contains
#         streamflow values for a week, and `y` contains them
#         for the following week
# Hint: Remember you can use `weekly_df.iloc` to index rows!

#TODO: Your code here
x = weekly_df1 = weekly_df.iloc[0:-1]
y = weekly_df2 = weekly_df.iloc[1:]


# %%
# Step 5: Verify that you can plot the data
# Note: You should just be able to run this cell directly,
#       no code modification is needed

plt.scatter(x, y )
plt.xlabel("Current week streamflow [cfs]")
plt.ylabel("Next week streamflow [cfs]")


# %%
# Step 6: Create a linear regression with scikit-learn
#         And use the `fit` function to map x -> y

#TODO: Your code here
full_regression = LinearRegression()
full_regression.fit(x,y)


# ...

# `np.around` rounds numbers to given number of digits
m = np.around(full_regression.coef_, 3)
b = np.around(full_regression.intercept_, 3)
r2 = np.around(full_regression.score(x,y), 3)
print('Regression equation is: y=mx+b')
print(f'    where m={m} and b={b}')
print(f'The r^2 value is {r2}')


# %%
# Step 7: Plot the regression line on the data
#         To do this, run `full_regression.predict` 
#         on the `x_sample` to produce `y_predicted`
# Note: You might get a warning here saying the regression
#       was fitted with feature names, that's okay!
x_sample = np.arange(0, 15000, 1000).reshape(-1, 1)


#TODO: Your code here
y_predicted = full_regression.predict(x_sample)

plt.scatter(x, y )
plt.plot(x_sample, y_predicted, color='black', label='Regression line')
plt.xlabel("Current week streamflow [cfs]")
plt.ylabel("Next week streamflow [cfs]")
plt.legend()


# %%
# Step 8: Create a `weekofyear` variable which just counts the week of year
# Note this is similar to the `dayofyear` variable we've seen in class

#TODO: Your code here
weekofyear = weekly_df.index.isocalendar().week


# %%
# Step 9: Select out columns with this week's week of year
#         along with next weeks and the following weeks
# Note: This week's week of year is 38

#TODO: Your code here
week1 = 38
week1_filter = weekly_df.index.isocalendar().week == week1
this_week = weekly_df[week1_filter]

week2 = 39
week2_filter = weekly_df.index.isocalendar().week == week2
next_week = weekly_df[week2_filter]

week3 = 40
week3_filter = weekly_df.index.isocalendar().week == week3
following_week = weekly_df[week3_filter]


# %%
# Step 10: Make a scatter plot of the two new datasets
# Note: You should just be able to run this cell directly,
#       no code modification is needed
plt.scatter(this_week, next_week, color='red', label='1 Week scatter')
plt.scatter(this_week, following_week, color='blue', label='2 Week scatter')
plt.xlabel('Current streamflow [cfs]')
plt.ylabel('Future streamflow [cfs]')


# %%
# Step 11: Make 2 new regression models. 
#          One that maps `this_week` to `next_week` and 
#          one that maps `this_week` to `following_week`

#TODO: Your code here
one_week_regression = LinearRegression()
one_week_regression.fit(this_week,next_week)
m2 = np.around(one_week_regression.coef_, 3)
b2 = np.around(one_week_regression.intercept_, 3)
r2_one_week = np.around(one_week_regression.score(x,y), 3)

print('Regression equation is: y=mx+b')
print(f'    where m={m2} and b={b2}')
print(f'The r^2 value is {r2_one_week}')


# ...
two_week_regression = LinearRegression()
two_week_regression.fit(this_week,following_week)

m3 = np.around(two_week_regression.coef_, 3)
b3 = np.around(two_week_regression.intercept_, 3)
r2_two_week = np.around(two_week_regression.score(x,y), 3)

print('Regression equation is: y=mx+b')
print(f'    where m={m2} and b={b2}')
print(f'The r^2 value is {r2_one_week}')


# ...

#%%
# Step 12: Use these regression models to make a prediction!
# Note: I've pulled out the last week from your data to make the
#       prediction with for you. I used [[-1]] so that the shape
#       matches what the model expects.
regression_input = weekly_df.iloc[[-1]]

# %%
#TODO: Your code here
one_week_prediction = one_week_regression.predict(regression_input)
two_week_prediction = two_week_regression.predict(regression_input)

print(f'One week prediction: {one_week_prediction.flatten()[0]}')
print(f'Two week prediction: {two_week_prediction.flatten()[0]}')

# %%
# Step 13: Copy these values into your streamflow forecast csv here:
# https://github.com/HAS-Tools-Fall2022/forecasting22/tree/main/forecast_entries

# CONGRATULATIONS! You finished!

# %%
