import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from datetime import datetime
from get_data import fetch_data_from_api
from data_processing import filter_data, preprocess_data, filter_data_daily, filter_data_weekly, filter_data_monthly, filter_data_hourly
from dateutil import parser
import plotly.express as px



def create_charts(df):


    return html.Div([

        html.Div([
            html.Div(id='current-dashboard-inputflow', 
                    style={'display':'inline-block', 'margin':'15px', 'border':'1px solid #ccc', 'padding':'20px', 'width':'20%', 'height':'30%', 'background-color':'#f9f9f9', 'font-weight':'bold', 'font-size':'20px'}),
            html.Div(id='current-dashboard-outputflow', 
                    style={'display':'inline-block', 'margin':'15px', 'border':'1px solid #ccc', 'padding':'20px', 'width':'20%', 'height':'30%', 'background-color':'#f9f9f9', 'font-weight':'bold', 'font-size':'20px'}),
            html.Div(id='current-dashboard-inputtds', 
                    style={'display':'inline-block', 'margin':'15px', 'border':'1px solid #ccc', 'padding':'20px', 'width':'20%', 'height':'30%', 'background-color':'#f9f9f9', 'font-weight':'bold', 'font-size':'20px'}),
            html.Div(id='current-dashboard-outputtds', 
                    style={'display':'inline-block', 'margin':'15px', 'border':'1px solid #ccc', 'padding':'20px', 'width':'20%', 'height':'30%', 'background-color':'#f9f9f9', 'font-weight':'bold', 'font-size':'20px'}),
        ], style={'margin':'20px 0', 'text-align': 'center'}),

        html.Div([
            html.Div(id='data-status', className='status-circle', style={
                'display':'flex',
                'margin':'15px', 
                'border':'1px solid #ccc', 
                'padding':'20px', 
                'width':'95%', 
                'height':'30%', 
                'background-color':'#f9f9f9', 
                'font-weight':'bold', 
                'font-size':'20px',
                'text-align':'center'}),
        ]),


         html.Div([
                html.Label('Report Type', style={'display':'block', 'margin-bottom':'5px', 'text-align':'right', 'margin-right':'10px'}),
                dcc.Dropdown(
                    id='report-type-dropdown',
                    options=[
                        {'label':'Show all', 'value':'show_all'},
                        {'label': 'Daily', 'value': 'daily'},
                        {'label': 'Weekly', 'value': 'weekly'},
                        {'label': 'Monthly', 'value': 'monthly'}
                    ],
                    value='show_all'
                )
            ], style={'width':'30%', 'display':'inline-block', 'text-align':'left'}),


        # Date selection
        html.Div([
            html.H3("Select Date Range", style={'text-align':'center', 'flex-grow':'1'}),
            html.Div([
                html.Label('From Date', style={'display':'block', 'margin-bottom':'5px', 'text-align':'right', 'margin-right':'10px'}),
                dcc.DatePickerSingle(
                    id='from-date-picker',
                    date=df['timestamp'].min(),
                    display_format='DD-MM-YYYY'
                )
            ], style={'width':'50%', 'display':'inline-block', 'text-align':'right'}),
            
            html.Div([
                html.Label('To Date', style={'display':'block', 'margin-bottom':'5px', 'text-align':'left', 'margin-right':'10px'}),
                dcc.DatePickerSingle(
                    id='to-date-picker',
                    date=df['timestamp'].max(),
                    display_format='DD-MM-YYYY'
                )
            ], style={'width':'50%', 'display':'inline-block', 'text-align':'right'}),

        ], style={'margin':'20px 0'}),    

        # Charts
        # html.Div([
            
        #     # Pie charts
        #     html.Div([
        #         dcc.Graph(id='pie-chart1')
        #     ], style={'width':'48%', 'display':'inline-block', 'margin':'0 1%'}),
            
        #     html.Div([
        #         dcc.Graph(id='pie-chart2')
        #     ], style={'width':'48%', 'display':'inline-block', 'margin':'0 1%'}),
            
        # ], style={'margin':'20px 0'}),

        html.Div([
            
            # Line charts
            html.Div([
                dcc.Graph(id='line-chart1')
            ], style={'width':'48%', 'display':'inline-block', 'margin':'0 1%'}),
            
            html.Div([
                dcc.Graph(id='line-chart2')
            ], style={'width':'48%', 'display':'inline-block', 'margin':'0 1%'}),
            
        ], style={'margin':'20px 0'}),

        # Button for descriptive stats page
        html.Div([
            html.Button('View Descriptive Stats', id='stats-button', n_clicks=0, style={'display':'block', 'margin':'20px auto', 'padding':'10px 20px', 'font-size':'16px', 'background-color':'#007BFF', 'color':'#fff', 'border':'none', 'border-radius':'4px', 'cursor':'pointer'})
        ], style={'text-align':'center'})

    ])

# Callback to update small boxes
def update_small_boxes_dashboard_callback(app, df):
    @app.callback(
        [
         Output('current-dashboard-inputflow', 'children'),
         Output('current-dashboard-outputflow', 'children'),
         Output('current-dashboard-inputtds', 'children'),
         Output('current-dashboard-outputtds', 'children'),],
         [Input('from-date-picker', 'date'),
        Input('to-date-picker', 'date')]
    )
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


# callback for operations mode
def operations_mode(app):
    @app.callback(
    Output('data-status', 'children'),
    [Input('from-date-picker', 'date'),
     Input('to-date-picker', 'date')]
    )
    def update_data_status(from_date, to_date):
        last_hour = pd.Timestamp.now() - pd.Timedelta(hours=1)
        last_24_hours = pd.Timestamp.now() - pd.Timedelta(hours=24)
        
        hourly_data = filter_data_hourly(from_date, to_date)
        
        if last_24_hours > hourly_data['timestamp'].iloc[-1]:
            return "🔴 Plant Operations Mode"
        elif last_hour > hourly_data['timestamp'].iloc[-1]:
            return "🟡 Plant Operations Mode"
        else:
            return "🟢 Plant Operations Mode"


        
    # Callback to update charts based on date selection
def update_charts_callback(app):    
    @app.callback(
        # [Output('pie-chart1', 'figure'),
        # Output('pie-chart2', 'figure'),
        [
        Output('line-chart1', 'figure'),
        Output('line-chart2', 'figure'),],
        [Input('from-date-picker', 'date'),
        Input('to-date-picker', 'date'),
        Input('report-type-dropdown', 'value')]
    )
    def update_charts(from_date, to_date, report_type):

        if report_type == 'daily':
            filtered_df = filter_data_daily(from_date, to_date)
        elif report_type == 'weekly':
            filtered_df = filter_data_weekly(from_date, to_date)
        elif report_type == 'monthly':
            filtered_df = filter_data_monthly(from_date, to_date)
        else:            
            filtered_df = filter_data(from_date, to_date)

        values2 = [(filtered_df['inputtds'] - filtered_df['outputtds']).mean(), (filtered_df['outputtds']).mean()]
        # Update pie charts
        # pie_chart1 = {
        #     'data': [go.Pie(
        #         labels=['Remaining', 'Output Flow'],
        #         values=[(filtered_df['inputflow'] - filtered_df['outputflow']).mean(), (filtered_df['outputflow']).mean()],
        #         hole=0.4,
        #         marker=dict(colors=['#3E87E3', '#74EAEC'])
        #     )],
        #     'layout': go.Layout(title='Water Flow')
        # }
        
        # pie_chart2 = {
        #     'data': [go.Pie(
        #         labels=['Remaining TDS', 'Output TDS'],
        #         values=values2,
        #         hole=0.4,
        #         marker=dict(colors=['#6F3E06', '#ECB974'])
        #     )],
        #     'layout': go.Layout(title='TDS')
        # }
        
        # Update line charts
        line_chart1 = {
            'data': [
                go.Scatter(x=filtered_df['timestamp'], y=filtered_df['inputflow'], mode='lines', name='Input Flow', line=dict(color='#3E87E3')),
                go.Scatter(x=filtered_df['timestamp'], y=filtered_df['outputflow'], mode='lines', name='Output Flow', line=dict(color='#74EAEC'))
            ],
            'layout': go.Layout(title='Input & Output Flow Over Time')
        }
        
        line_chart2 = {
            'data': [
                go.Scatter(x=filtered_df['timestamp'], y=filtered_df['inputtds'], mode='lines', name='Input TDS', line=dict(color='#6F3E06')),
                go.Scatter(x=filtered_df['timestamp'], y=filtered_df['outputtds'], mode='lines', name='Output TDS', line=dict(color='#ECB974'))
            ],
            'layout': go.Layout(title='Input & Output TDS Over Time')
        }
        
        
        return line_chart1, line_chart2

