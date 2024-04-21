#import dash_html_components as html
from dash import html
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
        [
         Output('current-inputflow', 'children'),
         Output('current-outputflow', 'children'),
         Output('current-inputtds', 'children'),
         Output('current-outputtds', 'children'),],
        [Input('table-from-date-picker', 'date'),
         Input('table-to-date-picker', 'date')]
    )
    # def update_small_boxes(from_date, to_date):
    #     filtered_df = filter_data(df, from_date, to_date)
    #     return (
    #             # f"Cumulative water consumed: {df['inputflow'].iloc[-1]} litres",
    #             f"Cumulative water dispensed: {df['outputflow'].iloc[-1]} litres",
    #             f"Current Input TDS: {df['inputtds'].iloc[-1]} ppm",
    #             f"Current Output TDS: {df['outputtds'].iloc[-1]} ppm",)
    def update_small_boxes(from_date, to_date):
        avg_input_tds = 0
        avg_output_tds = 0
        count_avg_input_tds = 0
        count_avg_output_tds = 0
        for i in range(1,7):
            if df['inputtds'].iloc[-i]:
                avg_input_tds+=df['inputtds'].iloc[-i]
                count_avg_input_tds+=1
            else:
                pass
            if df['outputtds'].iloc[-i]:
                avg_output_tds+=df['outputtds'].iloc[-i]
                count_avg_output_tds+=1
            else:
                pass
        avg_input_tds = (avg_input_tds)/(count_avg_input_tds)
        avg_output_tds = (avg_output_tds)/(count_avg_output_tds)
        return (
                # f"Cumulative water consumed: {df['inputflow'].iloc[-1]} litres",
                f"Total Water Served from Feb 13, 2024: {round((df['outputflow'].iloc[-1]-10000)/1000,2)} kl",
                f"Total Water Saved from Feb 13, 2024: {round((0.4*((df['inputflow'].iloc[-1]-10000)-(df['outputflow'].iloc[-1]-5000))-0.2*((df['inputflow'].iloc[-1]-10000)-(df['outputflow'].iloc[-1]-5000)))/1000,2)} kl",
                f"Current Input TDS (avg. over an hour): {round(avg_input_tds,2)} ppm",
                f"Current Output TDS (avg. over an hour): {round(avg_output_tds,2)} ppm")
                # f"Current Input TDS: {df['inputtds'].iloc[-1]} ppm",
                # f"Current Output TDS: {df['outputtds'].iloc[-1]} ppm")


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
