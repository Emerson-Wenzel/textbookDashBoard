'''
app.py


'''

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np

from query import *



sold_df = scan_table("SOLD_INVENTORY")

#replace 'na' class names with MISC
sold_df['Dept_1'].fillna('Misc', inplace=True)



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

app.layout = html.Div(
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
                    id = 'deptDropDown',
                    options=[
                        {'label': deptName, 'value': deptName}\
                        for deptName in sorted(set(sold_df['Dept_1']))
                    ],
                )
            ]
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id = 'classDropDown'
                )
             ]
        ),
        html.Div(id='tableID', style={'overflow': 'auto', 'height': '400px'}),


    ])

@app.callback(
    Output(component_id='classDropDown', component_property='options'),
    [Input(component_id='deptDropDown', component_property='value')]
)
def update_classDropDown(department):
    short_df = query_class(department)

    # TODO: Must be expanded to include all class numbers.
    # definitely other selling (Class_1-2, etc.), unsure about sold
    return [{'label': classNumber, 'value': classNumber} for classNumber in sorted(set(short_df['Class_1-1']))]


@app.callback(
    Output(component_id='tableID', component_property='children'),
    [Input(component_id='deptDropDown', component_property='value'),
     Input(component_id='classDropDown', component_property='value')]
)
def update_table(department, classNumber):
    short_df = query_class(department, classNumber)
    return generate_table(short_df)
    


if __name__ == '__main__':
    app.run_server(debug=True)
