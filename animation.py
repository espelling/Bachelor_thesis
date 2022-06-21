# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 17:49:49 2022

@author: estas
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv('dashboard_time_series_complete.csv', index_col=0)

def blank_fig():
    fig = px.scatter(x=None, y=None)  # width=800, height=350)
    fig.update_layout(
         title='Graph: Line chart')

    return fig

yAxis_options = []
for yOption in df.columns:
    yAxis_options.append({'label': str(yOption), 'value': yOption})



# Starte App
app = dash.Dash(__name__)


app.layout = html.Div(children=[
    
    html.Div(children=[
        dcc.Graph(
            id='graph',
            figure=blank_fig()
            #style={'height': '400px', 'width': '800px'}
        ),
        
    # Dropdown für Scatterplot -> X-Achse
    dcc.Dropdown(id='xAxes-scatterplot',
                 options=yAxis_options,
                 placeholder="X-axes",
                 multi=False,
                 style={'margin-top': '1vw'}
                 )
    ])
    
])


@app.callback(Output('graph', 'figure'), Input('xAxes-scatterplot', "value")
              )
def update_graph(input_test):
    fig = px.scatter(df, x="GNI_2019", y="Doses_admin_per_100", animation_frame="Date", animation_group="Country",
               size="Deaths_rel", color="Income group", hover_name="Country",
               log_x=True, size_max=55, range_x=[1,100000], range_y=[0,350])
    return fig
