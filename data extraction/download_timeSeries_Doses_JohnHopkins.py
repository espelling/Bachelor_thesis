import pandas as pd
import wget

# Der Quellcode bezogen aus der Quelle: https://towardsdatascience.com/covid-19-data-processing-58aaa3663f6
# verabreichte Impfdosen: Download der Daten (JHU) -> Url der Rohdaten im CSV-Format
urls = [
    'https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/global_data/time_series_covid19_vaccine_doses_admin_global.csv',
    'https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/global_data/time_series_covid19_vaccine_global.csv',
    'https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/global_data/vaccine_data_global.csv'
]
[wget.download(url) for url in urls]

