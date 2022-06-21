# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 13:28:52 2022

@author: estas
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
import datetime
from datetime import date


# Data Import
df_TS_world = pd.read_csv('dashboard_time_series_complete.csv', index_col=0)

# Spalten umbenennen
df_TS_world = df_TS_world.rename(columns={"Confirmed_Cases":"Cases total abs.", "Deaths":"Deaths total abs.", 
                                          "New_Cases":"Cases daily abs.", "New_Deaths":"Deaths daily abs.",
                                          "Doses_admin":"Doses vaccine admin. total",
                                          "Confirmed_Cases_rel":"Cases total %", "Deaths_rel":"Deaths total %",
                                          "Doses_admin_per_100":"Doses vaccine admin. / 100 persons",
                                          "GDP_pro_Kopf":"GDP per capita", "GNI_2019":"GNI per capita",
                                          "Income group":"Classification by income (World Bank)",
                                          "new_tests":"Tests daily abs.", "total_tests":"Tests total abs."})
# Spalten entfernen
df_TS_world = df_TS_world.drop(['_merge'], axis=1)

# --------------------------------Options for Dropdowns----------------------------------
# Dropdown Menü -> Optionen für County-Picker
country_options = []
for country in df_TS_world['Country'].unique():
    country_options.append({'label': str(country), 'value': country})

# Dropdown Menü -> Optionen für y-axis-picker-line-chart
yAxis_options = []
for yOption in df_TS_world.columns:
    yAxis_options.append({'label': str(yOption), 'value': yOption})


# ---------------------------------------------------------------------------------------

# Funktion -> initiales Figure für Line-Chart erstellen
def blank_fig():
    fig = px.line(x=None, y=None)  # width=800, height=350)
    fig.update_layout(
         title='Graph: Line chart')

    return fig

# Funktion -> initiales Figure für Scatterplot erstellen
def blank_fig_scatter():
    fig = px.scatter(x=None, y=None, size=None, log_x=False)
    fig.update_layout(
         title='Graph: Scatterplot')

    return fig


# Starte App
app = dash.Dash(__name__)

# ---------------------------------- LAYOUT ------------------------------------------------------------------------
# Haupt-Div
app.layout = html.Div(children=[
    
    # Hauptüberschrift
    html.Div(children=[
        html.H3(children='Exploratory Data Analysis App'),
        html.H6(children='COVID-19 pandemic data', style={
                'marginTop': '-15px', 'marginBottom': '0px'})
    ], style={'textAlign': 'left', 'margin-left':'2rem'}),

    # ----------------------LINE-CHART----------------------------

    # 1 Div - Line-Chart
    html.Div(children=[
        
        # 1.1 Anleitungs-Text
        html.Div(children=[
            
            # dcc.Textarea(
            #     id='textarea-line-chart',
            #     value='Textarea LINECHART'
            #     #style={'width': '150px', 'height': '210px'},
            # )
            html.P("Text area for Line chart"
                )
        ], className="two columns",
            style={'padding': '2rem', 'margin': '1rem', 'marginTop': '2rem', 'background-color': 'white'}),


        # 1.2 Graph - Line Chart
        html.Div(children=[
            dcc.Graph(
                id='line-chart',
                figure=blank_fig()
                #style={'height': '400px', 'width': '800px'}
            )
        ], className="six columns",
            style={'padding': '2rem', 'margin': '1rem', 'marginTop': '2rem', 'background-color': 'white'}),

        # 1.3 Inputs Line-Chart
        html.Div(children=[
            html.Label(
                'Choose countries and dimension:'
            ),

            # Dropdown für Line-Chart -> Country-Picker
            dcc.Dropdown(id='country-picker-line-chart',
                         options=country_options,
                         placeholder="Country",
                         multi=True,
                         style={'margin-top': '1vw'}
                         ),

            # Dropdown für Line-Chart -> Wert Y-Achse
            dcc.Dropdown(id='y-axis-picker-line-chart',
                         options=yAxis_options,
                         placeholder="Dimension y-axis",
                         multi=False,
                         clearable=True,
                         style={'margin-top': '1vw', 'margin-bottom': '2vw'}
                         ),

            html.Label('Choose start and end date:'),

            # Date-Picker Startdatum
            dcc.DatePickerSingle(
                id='date-picker-line-chart-start',
                placeholder="Start date",
                clearable=True,
                initial_visible_month=date(2022, 1, 1),
                style={'margin-top': '1vw'}
            ),

            # Date-Picker Enddatum
            dcc.DatePickerSingle(
                id='date-picker-line-chart-end',
                placeholder="End date",
                clearable=True,
                initial_visible_month=date(2022, 1, 1),
                style={'margin-top': '1vw'}
            )


        ], className="two columns",
            style={'padding': '2rem', 'margin': '1rem', 'marginTop': '2rem', 'background-color': 'white'}),

        # 1.4 Inputs Annotation
        html.Div(children=[

            # Annotation erstellen
            html.Label('Create annotation:'),

            # Date-Picker Datum Ereignis
            dcc.DatePickerSingle(
                id='date-picker-line-chart-annotation',
                placeholder="Select date",
                clearable=True,
                initial_visible_month=date(2022, 1, 1),
                style={'margin-top': '1vw'}
            ),

            # Text Input Ereignis
            dcc.Input(
                id='textInput-line-chart',
                placeholder='Description', 
                type='text',
                style={'margin-top': '1vw', 'margin-bottom': '1vw', 'width': '160px'
                }
            ),

            # Button : Bestätigen
            html.Button('Set as start', id='button-line-chart',
                        n_clicks=0,
                        # style={'background-color':'white',#'color':'white',
                        #        'height':'30px','width':'200px',
                        #        'margin-top':'1vw','margin-left':'0vw'}
                        )

        ], className="two columns",
            style={'padding': '2rem', 'margin': '1rem', 'marginTop': '2rem', 'margin-left': '6rem', 'background-color': 'white'})

    ], className="twelve columns", style={'background-color': 'white', 'width': '80%','margin-left':'2rem','margin-top': '2rem'}),

    # -------------------------SCATTERPLOT------------------------
    # 2 Div - Scatterplot
    html.Div(children=[
        
        # 2.1 Einleitung
        html.Div(children=[
            html.P("Text area for Scatterplot"
                )
        ], className="two columns",
            style={'padding': '2rem', 'margin': '1rem', 'marginTop': '2rem', 'background-color': 'white'}),
        
        # 2.2 Scatterplot
        html.Div(children=[
            dcc.Graph(
                id='scatterplot',
                figure=blank_fig_scatter()
                #style={'height': '500px', 'width': '800px'}
            )
        ], className="six columns",
            style={'padding': '2rem', 'margin': '1rem', 'marginTop': '2rem', 'background-color': 'white'}),

        # 2.3 Inputs Scatterplot
        html.Div([
            
            # Label
            html.Label('Choose the dimensions:'),

            # Dropdown für Scatterplot -> X-Achse
            dcc.Dropdown(id='xAxes-scatterplot',
                         options=yAxis_options,
                         placeholder="X-axes",
                         multi=False,
                         style={'margin-top': '1vw'}
                         ),

            # Dropdown für Scatterplot -> Y-Achse
            dcc.Dropdown(id='yAxes-scatterplot',
                         options=yAxis_options,
                         placeholder="Y-axes",
                         multi=False,
                         style={'margin-top': '1vw'}
                         ),

            # Dropdown für Scatterplot -> Punktgröße
            dcc.Dropdown(id='size-scatterplot',
                         options=yAxis_options,
                         placeholder="Dot size",
                         multi=False,
                         style={'margin-top': '1vw','margin-bottom': '2vw'}
                         ),
            
            # Label für Slider
            html.Label('Choose the date:'),
            
            # Date-Picker Datum Ereignis
            dcc.DatePickerSingle(
                id='date-picker-scatterplot',
                placeholder="Select date",
                clearable=True,
                initial_visible_month=date(2022, 1, 1),
                style={'margin-top': '1vw','margin-bottom': '1vw'}
            ),
            html.Div(children=[
                # Button : Datum + 1 Tag
                html.Button('Add a day', id='button-plus-scatterplot',
                            n_clicks=0)
            ])
            
        ], className="two columns",
            style={'padding': '2rem', 'margin': '1rem', 'marginTop': '2rem', 'background-color': 'white'}),
        
        # 1.4 Inputs Annotation
        html.Div(children=[

            # Annotation erstellen
            html.Label('Set axes to log:'),

            # Button : Bestätigen
            html.Button('Set X -> log', id='logX_scatterplot',
                        n_clicks=0,
                        style={'margin-top':'1vw'}
                        ),
            
            html.Button('Set Y -> log', id='logY_scatterplot',
                        n_clicks=0,
                        style={'margin-top':'1vw'}
                        ),

        ], className="two columns",
            style={'padding': '2rem', 'margin': '1rem', 'marginTop': '2rem', 'margin-left': '6rem', 'background-color': 'white'})
    ], className="twelve columns", style={'width': '80%','margin-left':'2rem','margin-top': '1rem','background-color': 'white'}),
    
    
    
    
])

# ---------------------------------- CALLBACK ---------------------------------------------------------------
# Server -> Line-Chart
@app.callback(Output('line-chart', 'figure'),
              Input('country-picker-line-chart', 'value'),
              Input('y-axis-picker-line-chart', 'value'),
              Input('date-picker-line-chart-start', 'date'),
              Input('date-picker-line-chart-end', 'date'),
              Input('date-picker-line-chart-annotation', 'date'),
              Input('textInput-line-chart', 'value'),
              Input('button-line-chart', 'n_clicks')
              )
def update_graph(selected_country, selected_yAxis_column, selected_date_start, selected_date_end, selected_date_annotation, name_annotation, button_clicked):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    fig = px.line(x=None, y=None)
    fig.update_layout(
         title='Graph: Line chart')

    # fig = go.Figure()
    # fig.update_layout(
    #     title='Überschrift Line-Chart',
    #     template = 'seaborn'
    #     )

    filtered_df = df_TS_world[df_TS_world['Country'].isin(selected_country)]
    date_max = df_TS_world['Date'].max()
    date_min = df_TS_world['Date'].min()

    for val in selected_country:
        help_df = filtered_df[filtered_df['Country'] == str(val)]
        fig.add_trace(go.Scatter(
            x=help_df["Date"],
            y=help_df[str(selected_yAxis_column)],
            mode="lines",
            name=str(val),
            line=dict(width=2),
            showlegend=True
        )
        )
        
        
        
        if triggered_id == 'button-line-chart':
            if (button_clicked % 2) != 0:
                if selected_date_annotation is None and selected_date_end is None:
                    fig.update_xaxes(title_text='Date', range=(date_min, date_max))
                if selected_date_annotation is not None and selected_date_end is None:
                    fig.update_xaxes(title_text='Date', range=(
                        selected_date_annotation, date_max))
                if selected_date_annotation is None and selected_date_end is not None:
                    fig.update_xaxes(title_text='Date', range=(
                        date_min, selected_date_end))
                if selected_date_annotation is not None and selected_date_end is not None:
                    fig.update_xaxes(title_text='Date', range=(
                        selected_date_annotation, selected_date_end))
                button_clicked = button_clicked-1

        else:
            # Start- und Enddatum setzen -> alle Varianten
            if selected_date_start is None and selected_date_end is None:
                fig.update_xaxes(title_text='Date', range=(date_min, date_max))
            if selected_date_start is not None and selected_date_end is None:
                fig.update_xaxes(title_text='Date', range=(
                    selected_date_start, date_max))
            if selected_date_start is None and selected_date_end is not None:
                fig.update_xaxes(title_text='Date', range=(
                    date_min, selected_date_end))
            if selected_date_start is not None and selected_date_end is not None:
                fig.update_xaxes(title_text='Date', range=(
                    selected_date_start, selected_date_end))

        # Achsentitel updaten
        fig.update_yaxes(title_text=str(selected_yAxis_column))
        fig.update_layout(
            title={
                'text': str(selected_yAxis_column) + ' / Date'
            }),

        # Annotation setzen
        if selected_date_annotation is not None:
            #print(type(selected_date_annotation))
            fig.add_vline(datetime.datetime.strptime(selected_date_annotation, '%Y-%m-%d').timestamp()*1000,
                          annotation_text=str(name_annotation), annotation_position="top right",
                          annotation_font_color=f'#ff7f7f', #annotation_textangle=90,
                          annotation_borderpad=10,
                          line_width=2, line_dash="dash", line_color=f'#ff7f7f'
            )
            
            # # Annotation -> Text
            # fig.add_annotation(
            #     x=selected_date_annotation, y=-10, text=str(name_annotation), yanchor='bottom', showarrow=False, arrowhead=1, arrowsize=1, arrowwidth=2, arrowcolor="#635563", ax=-20, ay=-30, font=dict(size=12, color="purple", family="Roboto"), align="left",)

            # # Annotation -> Linie
            # fig.update_layout(shapes=[dict(type='line',
            #                                yref='paper', y0=0, y1=1,
            #                                xref='x', x0=selected_date_annotation, x1=selected_date_annotation,
            #                                line=dict(color="MediumPurple",
            #                                          width=1,
            #                                          dash="dot")
            #                                ),
            #                           ])

        # Fußnote für Line-Chart
        fig.add_annotation(
        text = (f"@Enrico Spelling / 09.06.2022<br>Source: JHU CSSE")
        , showarrow=False
        , x = 0
        , y = 0
        , xref='paper'
        , yref='paper'
        , xanchor='left'
        , yanchor='bottom'
        , xshift=-1
        , yshift=-80
        , font=dict(size=10, color="grey")
        , align="left"
        ,)
    return fig


# Server -> Scatterplot
@app.callback(Output('scatterplot', 'figure'),
              Input('xAxes-scatterplot', 'value'),
              Input('yAxes-scatterplot', 'value'),
              Input('size-scatterplot', 'value'),
              Input('date-picker-scatterplot', 'date'),
              Input('button-plus-scatterplot', 'n_clicks'),
              Input('logX_scatterplot', 'n_clicks'),
              Input('logY_scatterplot', 'n_clicks'))
def update_graph2(selected_xAxes, selected_yAxes, selected_size, selected_date, button_plus, log_xaxes, log_yaxes):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    
    # Tage addieren
    if triggered_id == 'button-plus-scatterplot':
        # Auswahl Datum
        if selected_date is None:
            date_max = df_TS_world['Date'].max()
            data_scatter = df_TS_world[df_TS_world['Date'] == date_max]
        else:
            # Date: String to Datetime
            selected_date = datetime.datetime.strptime(selected_date, '%Y-%m-%d')
            
            # Date: Add a day
            date_DTformat = selected_date + datetime.timedelta(days=1*int(button_plus))
            
            # Date Datetime to String
            selected_date_2 = datetime.datetime.strftime(date_DTformat, '%Y-%m-%d')
            
            data_scatter = df_TS_world[df_TS_world['Date'] == selected_date_2]        
    else:
        if selected_date is None:
            date_max = df_TS_world['Date'].max()
            data_scatter = df_TS_world[df_TS_world['Date'] == date_max]
        else:
            data_scatter = df_TS_world[df_TS_world['Date'] == selected_date]

    # alle Werte "Income group" in String umwandeln
    data_scatter['Classification by income (World Bank)'] = data_scatter['Classification by income (World Bank)'].astype(str)

    # alle Werte "Income group"=0 -> umwandeln zu "unknown"
    data_scatter['Classification by income (World Bank)'] = data_scatter['Classification by income (World Bank)'].replace(
        '0', 'unknown')

    fig = px.scatter(data_scatter, x=selected_xAxes, y=selected_yAxes,
                     size=selected_size, hover_name="Country",
                     log_x=False, size_max=20, color='Classification by income (World Bank)',
                     trendline='lowess', trendline_scope='overall',
                     trendline_color_override='rgb(201, 201, 201)')
    
    fig.update_layout(
        title={
            'text': 'Date: ' + data_scatter['Date'].max()
        })
    
    if (log_xaxes % 2) != 0:
        fig.update_xaxes(type="log")
        
    if (log_yaxes % 2) != 0:
        fig.update_yaxes(type="log")
    
    # fig = go.Figure()
    # fig.update_layout(
    #     title='Überschrift Line-Chart',
    #     template = 'plotly_dark'
    #     )

    # #print(type(selected_xAxes))
    # print(data_scatter["Income group"])

    # fig.add_trace(go.Scatter(
    #         x = data_scatter[str(selected_xAxes)],
    #         y = data_scatter[str(selected_yAxes)],
    #         marker_size = data_scatter[str(selected_size)]*100,
    #         # marker_color = data_scatter["Income group"],
    #         # marker = {'color': data_scatter["Income group"],
    #         #           'colorscale': 'Viridis',
    #         #           'showscale':True,
    #         #           'size': 100
    #         #  },
    #         mode = "markers",
    #         name = data_scatter["Income group"].unique,
    #         line = dict(width = 2),
    #         showlegend = True
    #         ))

    # Fußnote für Line-Chart
    fig.add_annotation(
    text = (f"@Enrico Spelling / 09.06.2022<br>Source: JHU CSSE")
    , showarrow=False
    , x = 0
    , y = -0.15
    , xref='paper'
    , yref='paper'
    , xanchor='left'
    , yanchor='bottom'
    , xshift=-1
    , yshift=-30
    , font=dict(size=10, color="grey")
    , align="left"
    ,)

    return fig


if __name__ == '__main__':
    app.run_server()
