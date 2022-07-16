# Bachelor_thesis
A COVID-19 dashboard developed as part of my bachelor thesis, which was developed in Python. Frameworks and Libraries: Plotly Dash, Pandas, Numpy, Seaborn, Matplotlib, Tools: Jupyter Notebook, Spyder

## Instructions
All files required for the application are located in the project folder. To start the web application, run the Dashboard.py script.
You find all the data needed for the dashboard in the dashboard_time_series_complete.csv file.

To bring the data up to date, carry out the following steps:
1. Go to the data extraction folder an run: "download_timeSeries_Cases_JohnHopkins.py" for downloading the case data
2. Then run: "download_timeSeries_Doses_JohnHopkins.py" for downloading the vaccine data
3. Then run: "data_processing.py" for processing the data and creating the file "COVID-19-time-series-clean-complete.csv"
4. Copy and paste the file "COVID-19-time-series-clean-complete.csv" into the parent project folder
5. In the parent project folder run the file "DataProcessing_World_Daily.ipynb" by using Jupyter Notebook. The updated file "dashboard_time_series_complete.csv" will be created.
6. Now you can start the application again by running "Dashboard.py"
