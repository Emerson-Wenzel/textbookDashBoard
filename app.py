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

from query import *
import df_ops
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler

global query_interval

sold_df = scan_table("SOLD_INVENTORY")
selling_df = scan_table("INVENTORY")

master_list = df_ops.get_master_list(selling_df)


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



app = dash.Dash()

def get_layout():
    return html.Div(
        [
            html.Div(
                [
                    html.H1('TCU Senate Textbook Exchange'),
                ]
            ),

            html.Div(
                [
                    html.H3('Dropdown menu'),
                    dcc.Dropdown(
                        id = 'classDropDown',
                        options=[
                            {'label': className, 'value': className}\
                            for className in master_list
                        ],
                    )
                ]
            ),
            html.Div(id='tableID', style={'overflow': 'auto',
                                          'height': '400px'}),

            html.Div(id='minMax'),
        ])

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
