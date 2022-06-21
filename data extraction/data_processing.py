import pandas as pd
import numpy as np

#Loading dataset and extracting date list
confirmed_df = pd.read_csv('time_series_covid19_confirmed_global.csv')
deaths_df = pd.read_csv('time_series_covid19_deaths_global.csv')
recovered_df = pd.read_csv('time_series_covid19_recovered_global.csv')

#Notice that columns are all date from the 4th column onwards and to get the list of dates confirmed_df.columns[4:]
#Before merging, we need to use melt() to unpivot DataFrames from current wide format into long format. In other words, we are kinda transposing all date columns into values. Here are the main settings for that:
#Use ‘Province/State’, ‘Country/Region’, ‘Lat’, ‘Long’ as identifier variables. We will later use them for merging.
#Unpivot date columns (As we saw previously columns[4:]) with variable column ‘Date’ and value column ‘Confirmed’
dates = confirmed_df.columns[4:]
confirmed_df_long = confirmed_df.melt(
    id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
    value_vars=dates, 
    var_name='Date', 
    value_name='Confirmed'
)
deaths_df_long = deaths_df.melt(
    id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
    value_vars=dates, 
    var_name='Date', 
    value_name='Deaths'
)
recovered_df_long = recovered_df.melt(
    id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
    value_vars=dates, 
    var_name='Date', 
    value_name='Recovered'
)

# Probleme mit Zahlen von Kanada -> nicht nach Provinz, sondern nach Country gezaehlt
# recovered_df_long = recovered_df_long[recovered_df_long['Country/Region']!='Canada']

# After that, we use merge() to merge the 3 DataFrames one after another
# Merging confirmed_df_long and deaths_df_long
full_table = confirmed_df_long.merge(
  right=deaths_df_long, 
  how='left',
  on=['Province/State', 'Country/Region', 'Date', 'Lat', 'Long']
)
# Merging full_table and recovered_df_long
full_table = full_table.merge(
  right=recovered_df_long, 
  how='left',
  on=['Province/State', 'Country/Region', 'Date', 'Lat', 'Long']
)
# Now, we should get a full table with Confirmed, Deaths and Recovered columns

#4. Performing Data Cleaning
#There are 3 tasks we would like to do
#Converting Date from string to datetime
#Replacing missing value NaN
#Coronavirus cases reported from 3 cruise ships should be treated differently
#You probably already notice that the values in the new Date column are all string with m/dd/yy format. To convert Date values from string to datetime, let’s use DataFrame.to_datetime()
full_table['Date'] = pd.to_datetime(full_table['Date'])

# Missing values NaN can be detected by running full_table.isna().sum()

# We found a lot NaN in Province/State, and that makes sense as many countries only report the Country-wise data. However, there are 1,602 NaNs in Recovered and let’s replace them with 0.
full_table['Recovered'] = full_table['Recovered'].fillna(0)

#Apart from missing values, there are coronavirus cases reported from 3 cruise ships: Grand Princess, Diamond Princess and MS Zaandam. These data need to be extracted and treated differently due to Province/State and Country/Region mismatch over time. Here is what I was talking about:
# And here is how we extract the ship data.
ship_rows = full_table['Province/State'].str.contains('Grand Princess') | full_table['Province/State'].str.contains('Diamond Princess') | full_table['Country/Region'].str.contains('Diamond Princess') | full_table['Country/Region'].str.contains('MS Zaandam')
full_ship = full_table[ship_rows]

# And to get rid of ship data from full_table :
full_table = full_table[~(ship_rows)] 

#5. Data Aggregation
#So far, all the Confirmed, Deaths, Recovered are existing data from raw CSV dataset. Let’s add an active cases column Active, which is calculated by active = confirmed — deaths — recovered .
# Active Case = confirmed - deaths - recovered
full_table['Active'] = full_table['Confirmed'] - full_table['Deaths'] - full_table['Recovered']
# And here is what full_table looks like now.

# Next, let’s aggregate data into Country/Region wise and group them by Date and Country/Region.
full_grouped = full_table.groupby(['Date', 'Country/Region'])['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()

#sum() is to get the total count of ‘Confirmed’, ‘Deaths’, ‘Recovered’, ‘Active’ for the given Date and Country/Region.
#reset_index() reset the index and use the default one, which is Date and Country/Region.
#And here is what full_grouped looks like now

#Now let’s add day wise New cases, New deaths and New recovered by deducting the corresponding accumulative data on the previous day.
# new cases 
temp = full_grouped.groupby(['Country/Region', 'Date', ])['Confirmed', 'Deaths', 'Recovered']
temp = temp.sum().diff().reset_index()
mask = temp['Country/Region'] != temp['Country/Region'].shift(1)
temp.loc[mask, 'Confirmed'] = np.nan
temp.loc[mask, 'Deaths'] = np.nan
temp.loc[mask, 'Recovered'] = np.nan
# renaming columns
temp.columns = ['Country/Region', 'Date', 'New cases', 'New deaths', 'New recovered']
# merging new values
full_grouped = pd.merge(full_grouped, temp, on=['Country/Region', 'Date'])
# filling na with 0
full_grouped = full_grouped.fillna(0)
# fixing data types
cols = ['New cases', 'New deaths', 'New recovered']
full_grouped[cols] = full_grouped[cols].astype('int')
# 
full_grouped['New cases'] = full_grouped['New cases'].apply(lambda x: 0 if x<0 else x)

# And finally here is the full_grouped. Be aware of that this final output is Country-wise data with
#Confirmed, Deaths, Recovered and Active are cumulative data.
#New cases, New deaths and New Recovered are day wise data.
#This DataFrames is ordered by Date and Country/Region.

#Finally, you can save this final data to a CSV file:
full_grouped.to_csv('COVID-19-time-series-clean-complete.csv')


# Data Exploration!!!!!!
