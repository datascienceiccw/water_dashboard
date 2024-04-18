import dash_html_components as html
from dash import dcc
from dash.dependencies import Input, Output
from data_processing import filter_data, preprocess_data
import pandas as pd

df = preprocess_data()

def table_layout():
    return html.Div([
        
        # Small boxes with outlines
        html.Div([
            html.Div(id='current-inputflow', style={'display':'inline-block', 'margin':'10px', 'border':'1px solid #ccc', 'padding':'30px', 'background-color':'#f9f9f9', 'font-weight':'bold', 'font-size':'24px'}),
            html.Div(id='current-outputflow', style={'display':'inline-block', 'margin':'10px', 'border':'1px solid #ccc', 'padding':'30px', 'background-color':'#f9f9f9', 'font-weight':'bold', 'font-size':'24px'}),
            html.Div(id='current-inputtds', style={'display':'inline-block', 'margin':'10px', 'border':'1px solid #ccc', 'padding':'30px', 'background-color':'#f9f9f9', 'font-weight':'bold', 'font-size':'24px'}),
            html.Div(id='current-outputtds', style={'display':'inline-block', 'margin':'10px', 'border':'1px solid #ccc', 'padding':'30px', 'background-color':'#f9f9f9', 'font-weight':'bold', 'font-size':'24px'}),
        ], style={'margin':'20px 0'}),
        
        # Date selection with outlines
        html.Div([
            html.Div([
                html.Label('From Date', style={'display':'block'}),
                dcc.DatePickerSingle(
                    id='table-from-date-picker',
                    date=df['timestamp'].min(),
                    display_format='DD-MM-YYYY',
                    style={'width':'100%', 'padding':'10px'}
                )
            ], style={'width':'50%', 'display':'inline-block', }),
            
            html.Div([
                html.Label('To Date', style={'display':'block'}),
                dcc.DatePickerSingle(
                    id='table-to-date-picker',
                    date=df['timestamp'].max(),
                    display_format='DD-MM-YYYY',
                    style={'width':'100%', 'padding':'10px'}
                )
            ], style={'width':'50%', 'display':'inline-block',})
        ], style={'margin':'20px 0'}),
        
        # Table with outlines
        html.Div([
            html.Table(id='data-table', style={'border':'1px solid #ccc', 'width':'100%', 'border-collapse':'collapse'}),
        ], style={'margin':'20px 0'})
        
    ], style={'margin':'20px 0'})

# Callback to update small boxes
def update_small_boxes_callback(app):
    @app.callback(
        [Output('current-inputflow', 'children'),
         Output('current-outputflow', 'children'),
         Output('current-inputtds', 'children'),
         Output('current-outputtds', 'children'),],
        [Input('table-from-date-picker', 'date'),
         Input('table-to-date-picker', 'date')]
    )
    def update_small_boxes(from_date, to_date):
        filtered_df = filter_data(df, from_date, to_date)
        return (f"Current Input Flow: {df['inputflow'].iloc[-1]} litres",
                f"Current Output Flow: {df['outputflow'].iloc[-1]} litres",
                f"Current Input TDS: {df['inputtds'].iloc[-1]} ppm",
                f"Current Output TDS: {df['outputtds'].iloc[-1]} ppm",)

# Callback to update table
def update_table_callback(app):
    @app.callback(
        Output('data-table', 'children'),
        [Input('table-from-date-picker', 'date'),
         Input('table-to-date-picker', 'date')]
    )
    def update_table(from_date, to_date):
        filtered_df = filter_data(df, from_date, to_date)
        return generate_table(filtered_df)

# Function to generate table
def generate_table(dataframe, max_rows=10):
    dataframe = dataframe.rename(columns={'inputflow':'input flow (in l)', 'outputflow': 'output flow (in l)', 'inputtds':'input tds (in ppm)', 'outputtds':'output tds (in ppm)'})
    dataframe.drop(['output_fluoride', 'timestamp', '_id'], axis=1, inplace=True)
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns], style={'border':'1px solid #ccc', 'background-color':'#53E8E8', 'font-weight':'bold'})] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col], style={'border':'1px solid #ccc', 'padding':'8px', 'font-size':'16px'}) for col in dataframe.columns
        ], style={'background-color':'#ffffff'}) for i in range(min(len(dataframe), max_rows))],
        style={'border-collapse':'collapse', 'width':'100%'}
    )
