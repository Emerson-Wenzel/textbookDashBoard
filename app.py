'''
app.py


'''

import atexit
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.plotly as py
import rowdata
import time
import datetime

from query import *
import df_ops
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler

global query_interval

sold_df = scan_table("SOLD_INVENTORY")
selling_df = scan_table("INVENTORY")

master_list = df_ops.get_master_list(selling_df)

# constant variables
lower_bound = 5;
upper_bound = 10;
min_date = datetime.date(2015, 1, 1)

#replace 'na' class names with MISC
sold_df['Dept_1'].fillna('Misc', inplace=True)


#builds table from given dataframe
def generate_table(dataframe):
    columnNames = ['Item', 'Edition', 'Price']
    
    return html.Table(
        #Header
        [html.Tr([html.Th(col) for col in columnNames])] +

        #Body
        [html.Tr([html.Td(dataframe.iloc[i][col]) for col in columnNames
        ]) for i in range(len(dataframe))]
    )

# builds scatterplot from given dataframe
def generate_scatterplot(df):
  clean_df = df.loc[(df['Time_sold']) > min_date]

  # assign row to appropriate dataframe
  low_df = clean_df.loc[(df['Time_difference'] < lower_bound)]
  middle_df = clean_df.loc[(df['Time_difference'] >= lower_bound) & (df['Time_difference'] <= upper_bound)]
  high_df = clean_df.loc[(df['Time_difference'] > upper_bound)]
    
  low_string = 'less than ' + str(lower_bound) + ' days'
  middle_string = 'between ' + str(lower_bound) + ' and ' + upper_bound + ' days'
  high_string = 'more than ' + str(upper_bound) + ' days'

  # make 3 separate traces
  trace1 = go.Scatter(
    x = low_df['Time_sold'],
    y = low_df['Price'],
    name = low_string,
    mode = 'markers',
    text = df['Item'],
    marker = dict (
      size = 10,
      color = 'blue'
      )
    )

  trace2 = go.Scatter(
    x = middle_df['Time_sold'],
    y = middle_df['Price'],
    name = middle_string,
    mode = 'markers',
    text = df['Item'],
    marker = dict (
      size = 10,
      color = 'red')
    )

  trace3 = go.Scatter(
    x = high_df['Time_sold'],
    y = high_df['Price'],
    name = high_string,
    mode = 'markers',
    text = df['Item'],
    marker = dict (
      size = 10,
      color = 'green')
    )

  data = [trace1, trace2, trace3]

  layout = dict(
    title = 'Previously Sold Books',
    xaxis = dict(title = 'Date Sold', zeroline = True),
    yaxis = dict(title = 'Price ($)', zeroline = True)
    )

  fig = dict(data = data, layout = layout)

  return fig
   


app = dash.Dash()



def get_layout():
    return html.Div(
        [
            html.Div(id='body',
                     children=[
                         html.Div(
                             [
                                 html.H1('TCU Senate Textbook Exchange'),
                             ]
                         ),


                         html.H3('Dropdown menu'),
                         dcc.Dropdown(id = 'classDropDown',
                                                  options=[
                                                      {'label': className, 'value': className}\
                                                      for className in master_list
                                                  ],
                         ),
                         
                         html.Div(id='dashboard',
                                  children=[

                                      html.Div(id='left_col',
                                          children=[
                                              html.Div(id='left_filter'),
                                              html.Div(id='tableID', style={'overflow': 'auto',
                                                                            'height': '400px'}),
                                          ]
                                      ),

                                      

                                      html.Div(id='right_col',
                                               children=[
                                                   html.Div(id='minMedMax'),
                                                   dcc.Graph(id='my-graph'),                                               ]
                                      ),

                                  ],
                         ),
                     ]
            )
            ]
        )


app.layout = get_layout()

def invScanner():
    selling_df = scan_table("INVENTORY")


@app.callback(
    Output(component_id='tableID', component_property='children'),
    [Input(component_id='classDropDown', component_property='value')]
)
def update_table(dept_num):
    if dept_num is None:
        return
    short_df = df_ops.get_class_data(selling_df, dept_num)
    return generate_table(short_df)

@app.callback(
    Output(component_id='minMedMax', component_property='children'),
    [Input(component_id='classDropDown', component_property='value')]

)
def update_minMedMax(dept_num):
    if dept_num is None:
        return
    short_df = df_ops.get_class_data(selling_df, dept_num)
    minimum = df_ops.get_min(short_df)
    median = df_ops.get_median(short_df)
    maximum = df_ops.get_max(short_df)

    return html.Div(
        [ 
            html.H3(minimum),
            html.H3(median),
            html.H3(maximum)
        ]
        )

@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    [Input(component_id='classDropDown', component_property='value')]
)
def update_scatterplot(dept_num):
    if dept_num is None:
      return
    short_df = df_ops.get_class_data(sold_df, dept_num)
    return generate_scatterplot(short_df)


# Requery the database every *query_interval* minutes.
# This is to keep the dataframe fresh
query_interval = 10
sch = BackgroundScheduler()
sch.start()
sch.add_job(func = invScanner, 
            trigger = IntervalTrigger(minutes = query_interval),
            id = 'timed_query', name = 'Query every 10 min',
            replace_existing = True)
atexit.register(lambda: sch.shutdown())

if __name__ == '__main__':
    app.run_server(debug=True)
