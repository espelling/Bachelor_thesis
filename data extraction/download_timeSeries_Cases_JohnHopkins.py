import pandas as pd
import wget

# Der Quellcode bezogen aus der Quelle: https://towardsdatascience.com/covid-19-data-processing-58aaa3663f6
# bestätigte Corona-Fälle + Todes-Fälle + Genesenen-Fälle: Download der Daten (JHU) -> Url der Rohdaten im CSV-Format
urls = [
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv',
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
]
[wget.download(url) for url in urls]

