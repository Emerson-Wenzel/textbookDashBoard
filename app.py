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

short_df = query_class("CHEM", 1) #remove this when ready

#replace 'na' class names with MISC
sold_df['class'].fillna('Misc', inplace=True)

app = dash.Dash()





if __name__ == '__main__':
    app.run_server(debug=True)
