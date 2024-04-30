import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from datetime import datetime
from get_data import fetch_data_from_api
from data_processing import filter_data, preprocess_data, filter_data_daily, filter_data_weekly, filter_data_monthly, filter_data_hourly
from dateutil import parser
import plotly.express as px


def update_dials(df):
    filtered_hourly_data = filter_data_hourly()

    water_served = round((df['outputflow'].iloc[-1]-10000)/1000,2)
    water_saved = round((0.4*((df['inputflow'].iloc[-1]-10000)-(df['outputflow'].iloc[-1]-5000))-0.2*((df['inputflow'].iloc[-1]-10000)-(df['outputflow'].iloc[-1]-5000)))/1000,2)
    avg_input_tds = filtered_hourly_data['inputtds'].iloc[-1]
    avg_output_tds = filtered_hourly_data['outputtds'].iloc[-1]
    revenue = 0.25 * water_served * 1000

    return [
    {'title': 'Water Served (kl)', 'value': water_served, 'max_value': round((df['outputflow']-10000)/1000,2).max()},
    {'title': 'Water Saved (kl)', 'value': water_saved, 'max_value': round((0.4*((df['inputflow']-10000)-(df['outputflow']-5000))-0.2*((df['inputflow']-10000)-(df['outputflow']-5000)))/1000,2).max()},
    {'title': 'Current Input TDS (ppm)', 'value': avg_input_tds, 'max_value': filtered_hourly_data['inputtds'].max()},
    {'title': 'Current Output TDS (ppm)', 'value': avg_output_tds, 'max_value': filtered_hourly_data['outputtds'].max()},
    {'title': 'Revenue Generated (in ₹)', 'value': revenue, 'max_value': round((df['outputflow']-10000)/1000,2).max() * 0.25 * 1000},
]


def create_dials(df):
    dial_data = update_dials(df)
    dial_figures = []
    for dial in dial_data:
        dial_figures.append({
            'data': [
                go.Indicator(
                    mode='number+gauge',
                    value=dial['value'],
                    title=dial['title'],
                    gauge={'axis': {'range': [None, dial['max_value']]},
                           'threshold': {
                               'line': {'color': 'red', 'width': 4},
                               'thickness': 0.75,
                               'value': dial['value']
                           }
                    }
                )
            ], 'layout': go.Layout(height=300)
        })

    return html.Div([
        # Boxes layout
        html.Div([
            # Input Flow dial
            dcc.Graph(id='current-dashboard-inputflow', figure=dial_figures[0], style={'display': 'inline-block', 'width': '20%'}),
            # Output Flow dial
            dcc.Graph(id='current-dashboard-outputflow', figure=dial_figures[1], style={'display': 'inline-block', 'width': '20%'}),
            # Input TDS dial
            dcc.Graph(id='current-dashboard-inputtds', figure=dial_figures[2], style={'display': 'inline-block', 'width': '20%'}),
            # Output TDS dial
            dcc.Graph(id='current-dashboard-outputtds', figure=dial_figures[3], style={'display': 'inline-block', 'width': '20%'}),
            dcc.Graph(id='revenue-generated', figure=dial_figures[4], style={'display': 'inline-block', 'width': '20%'}),
        ], style={'margin': '10px 0', 'text-align': 'center'}),
    ], style={'background-color':'#F3F3F3'})


def create_table_chart(df):
    # Create the table data
    daily_data = filter_data_daily(str(df['timestamp'].max() - pd.Timedelta(days=15)), str(df['timestamp'].max()))
    daily_water_served = int((daily_data['outputflow'].iloc[-1]-10000) / 20)

    message = ''

    last_hour = pd.Timestamp.now() - pd.Timedelta(hours=1)
    last_24_hours = pd.Timestamp.now() - pd.Timedelta(hours=24)
    
    hourly_data = filter_data_hourly()
    
    if last_24_hours > hourly_data['timestamp'].iloc[-1]:
        message = "🔴 Stopped"
    elif last_hour > hourly_data['timestamp'].iloc[-1]:
        message = "🟡 Standby"
    else:
        message = "🟢 Running"
    table_data = {
        'Plant Details': [
            'Site Name: Gandhipura',
            'Capacity of Plant: Your Plant Capacity',
            'Technology: CDI Technology',
            'Population: 2xxxx',
            f'Impact Reached: {daily_water_served * 4}',
            f'Plant Current Running Status: {message}'
        ]
    }

    # Create table rows with separator border lines
    table_rows = [html.Tr(html.Td(detail, style={'borderBottom': '1px solid #000000', 'padding': '20px'})) for detail in table_data['Plant Details']]

    # Create the table
    table = html.Div([
        html.H3('Plant Details'),
        html.Table(
            # Table body
            [html.Tbody(table_rows)],
            style={'width':'100%', 'backgroundColor': '#FFFFFF'}
        )
    ], style={'padding': '20px', 'margin': '10px', 'width': '85%'})

    # Create combined chart
    fig = go.Figure()
    
    # Add grouped bar chart
    fig.add_trace(
        go.Bar(x=daily_data['timestamp'], y=daily_data['inputflow'] / 1000, name='Input Flow'),
    )
    fig.add_trace(
        go.Bar(x=daily_data['timestamp'], y=daily_data['outputflow'] / 1000, name='Output Flow'),
    )
    
    # Add line chart
    fig.add_trace(
        go.Scatter(x=daily_data['timestamp'], y=daily_data['outputtds'], yaxis='y2', name='Output TDS', mode='lines'),
    )

    fig.update_layout(height=500, showlegend=True,
                      title='Daily Water Input and Output Flow with Average Output TDS',
                      xaxis=dict(title='Timestamp', tickfont=dict(size=14)),
                      yaxis=dict(title='Water Volume (in kl)', side='left', showgrid=False, tickfont=dict(size=12)),
                      yaxis2=dict(title='Output TDS (in ppm)', overlaying='y', side='right', range=[daily_data['outputtds'].min(), daily_data['outputtds'].max()], showgrid=False, tickfont=dict(size=12)),)
    
    return html.Div([
        # Plant details table
        html.Div([
            table
        ], style={'background-color': '#F3F3F3', 'float': 'left', 'width': '27%'}),

        # Combined chart
        html.Div([
            dcc.Graph(id='combined-chart', figure=fig)
        ], style={'float': 'left', 'width': '73%'})
    ])


