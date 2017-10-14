
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np



availBooks_df = pd.read_csv(r'new_selling.csv')
#soldBooks_df = pd.read_csv(r'C:\Users\emers\Desktop\programming\Projects\dash\TBE\soldTextBooks.csv')


###Clean up the data
#Remove $ from prices
availBooks_df['price'] = availBooks_df['price'].str.strip('$')
#soldBooks_df['Price'] = availBooks_df['Price'].str.strip('$')

#Fill the blank class names with "Misc"
availBooks_df['class'].fillna('Misc', inplace=True)

#classList = set()
#classList.add(className for className in availBooks_df['ClassName'])


#Start app
app = dash.Dash()



#Function to generate table, this can show any dataframe
def generate_table(dataframe):
    return html.Table(
        #Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        #Body
        [html.Tr([html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(len(dataframe))]
    )



def generate_histogram(df):
    return {
        'data':[go.Histogram(
            x = df['price'],
            xbins=dict(
                start=0,
                end = 200,
                size = 10
            )
            
        )],
        'layout':{
            'height': 600,
            'width': 1000
        }
    }


#app = dash.Dash()

app.layout = html.Div(
    [
        html.Div(
            [
                html.H4(children='Books'),

            ]

        ),
        
        html.Div(
            [
                html.H1('Dropdown menu'),
                dcc.Dropdown(
                    id='classDropDown',
                    options=[
                        {'label': className, 'value': className} \
                        for className in sorted(set(availBooks_df['class']))                          
                    ],
                    
                    multi=True,
                )
            ]    
        ),

        html.Div(
            [
                html.Div(id='tableID', style={'overflow': 'auto', 'height': '400px'})
            ]
        ),
        
        html.Div(
            [
                dcc.Graph(id='histogramID')
            ]
        )
    
        
            
    ])

@app.callback(
    Output(component_id='tableID', component_property='children'),
    [Input(component_id='classDropDown', component_property='value')]
)


def update_table(classNameArray):
    print(classNameArray)
    bookIndices = np.zeros((availBooks_df.shape[0]), dtype=bool);
    for className in classNameArray:
        bookIndices = (availBooks_df['class'] == className) | bookIndices
        
    short_df = availBooks_df[bookIndices]
    
    return generate_table(short_df)

    
@app.callback(
    Output('histogramID', 'figure'),
    [Input('classDropDown', 'value')]
)


def update_histrogram(classNameArray):
    bookIndices = np.zeros((availBooks_df.shape[0]), dtype=bool);
    for className in classNameArray:
        bookIndices = (availBooks_df['class'] == className) | bookIndices
        
    short_df = availBooks_df[bookIndices]
    
    return generate_histogram(short_df)
    

if __name__ == '__main__':
    app.run_server(debug=True)





'''
                #generate_table(availBooks_df)
                dcc.Graph(
                    figure={
                        'data':[go.Histogram(
                            x=availableBooks_df['Price']
                        )],
                    
                    'layout': {
                    'title':'TextBook Prices'
                    }
                    }
                    

   ''' 
