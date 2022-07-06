# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 13:28:52 2022

@author: Enrico Spelling Mat.Nr. 572730
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
from plotly.subplots import make_subplots
from scipy import signal


# Data Import
df_TS_world = pd.read_csv('dashboard_time_series_complete.csv', index_col=0)

# Spalten umbenennen
df_TS_world = df_TS_world.rename(columns={"Confirmed_Cases":"Cases total abs.", "Deaths":"Deaths total abs.", 
                                          "New_Cases":"Cases daily abs.", "New_Deaths":"Deaths daily abs.",
                                          "Doses_admin":"Doses vaccine admin. total",
                                          "Confirmed_Cases_rel":"Cases total relative", "Deaths_rel":"Deaths total relative",
                                          "Doses_admin_per_100":"Doses vaccine admin. / 100 persons",
                                          "GDP_pro_Kopf":"GDP per capita", "GNI_2019":"GNI per capita",
                                          "Income group":"Classification by income",
                                          "new_tests":"Tests daily abs.", "total_tests":"Tests total abs.", "total_tests_rel":"Tests total relative"})

# alle Werte "Income group" = 0 -> umbenennen
df_TS_world['Classification by income']= df_TS_world['Classification by income'].replace('0', 'unknown')



# ----------------------------------------------Optionen für Dropdowns----------------------------------
# Dropdown Menü -> Optionen für County-Picker
country_options = []
for country in df_TS_world['Country'].unique():
    country_options.append({'label': str(country), 'value': country})

# Dropdown Menü -> Optionen für Y-Achse
yAxis_options = []
for yOption in df_TS_world.columns:
    yAxis_options.append({'label': str(yOption), 'value': yOption})



# -----------------------------------------------initale Figures----------------------------------------
# Funktion -> initiales Figure für Line-Chart erstellen
def blank_fig():
    fig = px.line(x=None, y=None)
    fig.update_layout(
         title='Graph: Line chart')

    return fig

# Funktion -> initiales Figure für Scatterplot erstellen
def blank_fig_scatter():
    fig = px.scatter(x=None, y=None, size=None, log_x=False)
    fig.update_layout(
         title='Graph: Scatterplot')

    return fig

# Funktion -> initiales Figure für Animation erstellen
def fig_video():
    
    fig = px.scatter(df_TS_world, x="GNI per capita", y="Doses vaccine admin. / 100 persons", animation_frame="Date", animation_group="Country",
           size="Cases total relative", color="Classification by income", hover_name="Country",
           log_x=True, size_max=55, range_x=[100,100000], range_y=[-20,350],
           height=700, width=1400)
    fig.update_layout(
         title="Animation: GNI per capita / Doses vaccine admin./100 persons / Cases total relative classsified by income (world bank) from 2020-01-22 until 2022-05-31",
         font=dict(
             size=10))
    # Speed control
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 10

    return fig


#-----------------------------------------------------START----------------------------------------------

# Starte App
app = dash.Dash(__name__)

# ----------------------------------------------------- LAYOUT ---------------------------------------------------------------------------------
# Haupt-Div
app.layout = html.Div(children=[
    
    # Hauptüberschrift
    html.Div(children=[
        html.H3(children='Exploratory Data Analysis App'),
        html.H6(children='COVID-19 pandemic data', style={
                'marginTop': '-15px', 'marginBottom': '0px'})
    ], style={'textAlign': 'left', 'margin-left':'2rem'}),

    # -------------------------------------LINE-CHART--------------------------------------------

    # 1 Div - Line-Chart
    html.Div(children=[
        
        # 1.1 Anleitungs-Text
        html.Div(children=[

            html.P(children=["Line Chart"],
                   style={'font-size': 15, 'font-family': 'Arial Black'}
                ),
            html.P(children=[html.Br(),"The following input fields are available:", html.Br(),html.Br(),"Country => Set the countries", html.Br(),"Dimension => Set the dimension", html.Br(),html.Br(),"Graph 2 is optional and adds a secondary y-axis.", html.Br(),html.Br(),"Start date => Set a start date", html.Br(),"End date => Set an end date", html.Br(),html.Br(),html.Br(),"Additionally, 2 annotations can be set:", html.Br(),html.Br(),"Select date => Set the date", html.Br(),"Description => Enter a text", html.Br(),"Set as start => Sets the annotation date as start date", html.Br(),html.Br(),html.Br(),"Further functions (download, zoom...) are available by hovering over the chart toolbar."],
                   style={'font-size': 10,
                          'text-align': 'left'}
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
                'Choose countries and dimensions:'
            ),

            # Dropdown für Line-Chart -> Country-Picker 1
            dcc.Dropdown(id='country-picker-line-chart',
                         options=country_options,
                         placeholder="Graph 1: Country",
                         multi=True,
                         style={'margin-top': '0.5vw'}
                         ),

            # Dropdown für Line-Chart -> Wert Y-Achse 1
            dcc.Dropdown(id='y-axis-picker-line-chart',
                         options=yAxis_options,
                         placeholder="Graph 1: Dimension",
                         multi=False,
                         clearable=True,
                         style={'margin-top': '0.5vw', 'margin-bottom': '1vw'}
                         ),
            
            # Dropdown für Line-Chart -> Country-Picker 2
            dcc.Dropdown(id='country-picker-line-chart-2',
                         options=country_options,
                         placeholder="Graph 2: Country",
                         multi=True,
                         style={'margin-top': '0.5vw'}
                         ),

            # Dropdown für Line-Chart -> Wert Y-Achse 1
            dcc.Dropdown(id='y-axis-picker-line-chart-2',
                         options=yAxis_options,
                         placeholder="Graph 2: Dimension",
                         multi=False,
                         clearable=True,
                         style={'margin-top': '0.5vw', 'margin-bottom': '1vw'}
                         ),

            html.Label('Choose start and end date:'),

            # Date-Picker Startdatum
            dcc.DatePickerSingle(
                id='date-picker-line-chart-start',
                placeholder="Start date",
                clearable=True,
                initial_visible_month=date(2022, 1, 1),
                style={'margin-top': '0.5vw'}
            ),

            # Date-Picker Enddatum
            dcc.DatePickerSingle(
                id='date-picker-line-chart-end',
                placeholder="End date",
                clearable=True,
                initial_visible_month=date(2022, 1, 1),
                style={'margin-top': '0.5vw'}
            )


        ], className="two columns",
            style={'padding': '2rem', 'margin': '1rem', 'marginTop': '2rem', 'background-color': 'white'}),

        # 1.4 Inputs Annotation
        html.Div(children=[

            # Annotation 1 erstellen
            html.Label('Create annotation 1:'),

            # Date-Picker Datum Ereignis 1
            dcc.DatePickerSingle(
                id='date-picker-line-chart-annotation',
                placeholder="Select date",
                clearable=True,
                initial_visible_month=date(2022, 1, 1),
                style={'margin-top': '0.5vw'}
            ),

            # Text Input Ereignis 1
            dcc.Input(
                id='textInput-line-chart',
                placeholder='Description', 
                type='text',
                style={'margin-top': '0.5vw', 'margin-bottom': '0.5vw', 'width': '160px'
                }
            ),

            # Button : Bestätigen 1
            html.Button('Set as start', id='button-line-chart',
                        n_clicks=0,
                        ),
            
            # Annotation 2 erstellen
            html.Label('Create annotation 2:',
                       style={'margin-top': '1vw'}),

            # Date-Picker Datum Ereignis 2
            dcc.DatePickerSingle(
                id='date-picker-line-chart-annotation-2',
                placeholder="Select date",
                clearable=True,
                initial_visible_month=date(2022, 1, 1),
                style={'margin-top': '0.5vw'}
            ),

            # Text Input Ereignis 2
            dcc.Input(
                id='textInput-line-chart-2',
                placeholder='Description', 
                type='text',
                style={'margin-top': '0.5vw', 'margin-bottom': '0.5vw', 'width': '160px'
                }
            ),

            # Button : Bestätigen 2
            html.Button('Set as start', id='button-line-chart-2',
                        n_clicks=0,
                        ),

        ], className="two columns",
            style={'padding': '2rem', 'margin': '1rem', 'marginTop': '2rem', 'margin-left': '6rem', 'background-color': 'white'})

    ], className="twelve columns", style={'background-color': 'white', 'width': '80%','margin-left':'2rem','margin-top': '2rem'}),
    
    
    

    # ------------------------------------SCATTERPLOT--------------------------------------------
    # 2 Div - Scatterplot
    html.Div(children=[
        
        # 2.1 Einleitung
        html.Div(children=[
            html.P(children=["Scatter Plot"],
                   style={'font-size': 15, 'font-family': 'Arial Black'}
                ),
            html.P(children=[html.Br(),"The following input fields are available:", html.Br(),html.Br(),"X-axes => Set the dimension for the X-axes", html.Br(),"Y-axes => Set the dimension for the Y-axes", html.Br(),"Dot size => Set the dimension for the dot size",html.Br(),html.Br(),html.Br(),"You can select a date on which the data will be displayed.", html.Br(),html.Br(),"Select date => Set the date", html.Br(),"Add a day => Press to go forward one day", html.Br(),html.Br(),html.Br(),"Additionally, you can set the state of the axes (linear or log)", html.Br(),html.Br(),"Set x -> log => Press to set x-axis as log", html.Br(),"Set y -> log => Press to set y-axis as log"],
                   style={'font-size': 10,
                          'text-align': 'left'}
               )
        ], className="two columns",
            style={'padding': '2rem', 'margin': '1rem', 'marginTop': '2rem', 'background-color': 'white'}),
        
        # 2.2 Scatterplot
        html.Div(children=[
            dcc.Graph(
                id='scatterplot',
                figure=blank_fig_scatter()
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
        
        # 2.4 Inputs Achsen-Formatierung
        html.Div(children=[

            # Überschrift
            html.Label('Set axes to log:'),

            # Buttons : Log X und Y
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
    ], className="twelve columns", style={'height': '200%','width': '80%','margin-left':'2rem','margin-top': '1rem','background-color': 'white'}),
    
    
    
    
    # ------------------------------------------Animation-----------------------------------------------
    # 3 Div - Animation
    html.Div(children=[
        
        # 3.1 Einleitung
        html.Div(children=[
            html.P(children=["Animation"],
                   style={'font-size': 15, 'font-family': 'Arial Black'}
                ),
            html.P(children=[html.Br(),"This animation can be used to better analyze the development of the vaccine dose distribution over time. The following dimensions are defined:", html.Br(),html.Br(),"X-axes = GNI per capita", html.Br(),"Y-axes = Doses vaccine admin. / 100 persons", html.Br(),"Dot size => Corona cases total relative to population",html.Br(),html.Br(),"Press the start button to start / stop button to pause the animation"],
                   style={'font-size': 10,
                          'text-align': 'left'}
               )
        ], className="two columns",
            style={'padding': '2rem', 'margin': '1rem', 'marginTop': '2rem', 'background-color': 'white'}),
        
        # 3.2 Animation
        html.Div(children=[
            dcc.Graph(
                id='videoplot',
                figure=fig_video()
            )
        ], className="ten columns",
            style={'padding': '2rem', 'margin': '1rem', 'marginTop': '2rem', 'background-color': 'white'}),
        
    ], className="twelve columns", style={'height': '200%','width': '80%','margin-left':'2rem','margin-top': '1rem','background-color': 'white'}),   
])

# ------------------------------------------------ CALLBACKS ---------------------------------------------------------------
# Server -> Line-Chart
@app.callback(Output('line-chart', 'figure'),
              Input('country-picker-line-chart', 'value'),
              Input('y-axis-picker-line-chart', 'value'),
              Input('country-picker-line-chart-2', 'value'),
              Input('y-axis-picker-line-chart-2', 'value'),
              Input('date-picker-line-chart-start', 'date'),
              Input('date-picker-line-chart-end', 'date'),
              Input('date-picker-line-chart-annotation', 'date'),
              Input('textInput-line-chart', 'value'),
              Input('button-line-chart', 'n_clicks'),
              Input('date-picker-line-chart-annotation-2', 'date'),
              Input('textInput-line-chart-2', 'value'),
              Input('button-line-chart-2', 'n_clicks')
              #Input('button-line-chart-overlay', 'n_clicks')
              )
def update_graph(selected_country, selected_yAxis_column, selected_country_2, selected_yAxis_column_2, selected_date_start, selected_date_end, selected_date_annotation, name_annotation, button_clicked, selected_date_annotation_2, name_annotation_2, button_clicked_2):#, button_clicked_overlay):
    # String-Wert aus dem Trigger holen
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Line-Chart Figure erstellen
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Überschrift Line-Chart
    fig.update_layout(
         title='Graph: Line chart', xaxis2= {'anchor': 'y', 'overlaying': 'x', 'side': 'top'})
    
    # nach ausgewählten Ländern filtern -> Fig 1
    filtered_df = df_TS_world[df_TS_world['Country'].isin(selected_country)]
    # Min + Max Datum wählen
    date_max = df_TS_world['Date'].max()
    date_min = df_TS_world['Date'].min()
    
    # Line-Chart befüllen -> Fig 1
    for val in selected_country:
        help_df = filtered_df[filtered_df['Country'] == str(val)]
        fig.add_trace(go.Scatter(
            x=help_df["Date"],
            # Glättung der Y-Werte mit Savitzky–Golay Filter
            #y=signal.savgol_filter(help_df[str(selected_yAxis_column)], 51, 3),
            y= help_df[str(selected_yAxis_column)],
            mode="lines",
            name=str(val),
            line=dict(width=1),
            showlegend=True),
        secondary_y=False
        )
        # Annotation 1
        # Wenn der Trigger vom Button-Line-Chart kommt und dessen Wert ungerade ist, dann Datum von Annotation setzen
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
        # Annotation 2
        # Wenn der Trigger vom Button-Line-Chart kommt und dessen Wert ungerade ist, dann Datum von Annotation setzen
        elif triggered_id == 'button-line-chart-2':
            if (button_clicked_2 % 2) != 0:
                if selected_date_annotation_2 is None and selected_date_end is None:
                    fig.update_xaxes(title_text='Date', range=(date_min, date_max))
                if selected_date_annotation_2 is not None and selected_date_end is None:
                    fig.update_xaxes(title_text='Date', range=(
                        selected_date_annotation_2, date_max))
                if selected_date_annotation_2 is None and selected_date_end is not None:
                    fig.update_xaxes(title_text='Date', range=(
                        date_min, selected_date_end))
                if selected_date_annotation_2 is not None and selected_date_end is not None:
                    fig.update_xaxes(title_text='Date', range=(
                        selected_date_annotation_2, selected_date_end))
                button_clicked_2 = button_clicked_2-1
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
        fig.update_yaxes(title_text=str(selected_yAxis_column), secondary_y=False)
        fig.update_layout(
            title={
                'text': str(selected_yAxis_column) + ' / Date'
            }),
        # Annotation 1 setzen
        if selected_date_annotation is not None:
            fig.add_vline(datetime.datetime.strptime(selected_date_annotation, '%Y-%m-%d').timestamp()*1000,
                          annotation_text=str(name_annotation), annotation_position="top right",
                          annotation_font_color='black',#f'#ff7f7f', #annotation_textangle=90,
                          annotation_borderpad=10,
                          line_width=2, line_dash="dash", line_color='black',#f'#ff7f7f'
            )
        # Annotation 2 setzen
        if selected_date_annotation_2 is not None:
            fig.add_vline(datetime.datetime.strptime(selected_date_annotation_2, '%Y-%m-%d').timestamp()*1000,
                          annotation_text=str(name_annotation_2), annotation_position="top right",
                          annotation_font_color='gray',#f'#ff7f7f', #annotation_textangle=90,
                          annotation_borderpad=10,
                          line_width=2, line_dash="dash", line_color='gray',#f'#ff7f7f'
            )
        # Fußnote für Line-Chart
        fig.add_annotation(
        text = (f"@Enrico Spelling / Source: JHU CSSE<br>" + str(date.today()))
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
     
        
    # Fig 2
    if selected_country_2 is not None:
        # nach ausgewählten Ländern filtern -> Fig 2
        filtered_df_2 = df_TS_world[df_TS_world['Country'].isin(selected_country_2)]
        # Min + Max Datum wählen
        date_max = df_TS_world['Date'].max()
        date_min = df_TS_world['Date'].min()
        # Line-Chart befüllen -> Fig 2
        for val in selected_country_2:
            help_df_2 = filtered_df_2[filtered_df_2['Country'] == str(val)]
            fig.add_trace(go.Scatter(
                x=help_df_2["Date"],
                # Glättung der Y-Werte mit Savitzky–Golay Filter
                # y=signal.savgol_filter(help_df_2[str(selected_yAxis_column_2)], 51, 3),
                y=help_df_2[str(selected_yAxis_column_2)],
                mode="lines",
                name=str(val) + " 2.axis",
                line=dict(width=1, dash='dot'),
                showlegend=True),
            secondary_y=True
            ),
            fig.update_yaxes(
                title_text=str(selected_yAxis_column_2), secondary_y=True, color= "gray")
            #fig.data[1].update(xaxis='x2')
            fig.update_layout(
                title={
                    'text': str(selected_yAxis_column) + ' and '+str(selected_yAxis_column_2)+' / Date'
                })
                 
    return fig

#---------------------------------------------------------------------------------------------------------------------------
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
            if selected_size == "Tests daily abs." or selected_size == "Tests total abs." or selected_size == "Tests total relative":
                data_scatter = df_TS_world[df_TS_world['Date'] == "2022-05-01"]
                print("Test-Data arrived-----------------------------")
            else:
                date_max = df_TS_world['Date'].max()
                data_scatter = df_TS_world[df_TS_world['Date'] == date_max]
            
        else:
            data_scatter = df_TS_world[df_TS_world['Date'] == selected_date]
            
            
    # alle Werte "Income group" in String umwandeln
    data_scatter['Classification by income'] = data_scatter['Classification by income'].astype(str)

    fig = px.scatter(data_scatter, x=selected_xAxes, y=selected_yAxes,
                      size=selected_size, hover_name="Country",
                      log_x=False, size_max=20, color='Classification by income',
                      trendline='lowess', trendline_scope='overall',
                      trendline_color_override='rgb(201, 201, 201)')
    
    fig.update_layout(
        title={
            'text': str(selected_xAxes) + ' / ' + str(selected_yAxes) + ' / ' + str(selected_size)+' on ' + data_scatter['Date'].max()
        })
    
    if (log_xaxes % 2) != 0:
        fig.update_xaxes(type="log")
        
    if (log_yaxes % 2) != 0:
        fig.update_yaxes(type="log")

    #Fußnote für Line-Chart
    fig.add_annotation(
    text = (f"@Enrico Spelling / Source: JHU CSSE<br>" + str(date.today()))
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
