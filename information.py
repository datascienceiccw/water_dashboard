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


def create_widgets(df):
    return html.Div([
        create_dials(df),
        create_table_chart(df)
    ], style={'background-color':'#6E716E', 'color': '#FFFFFF'})


def update_dials(df):
    filtered_hourly_data = filter_data_hourly()

    water_served = round((df['outputflow'].iloc[-1]-10000)/1000,2)
    water_saved = round((0.4*((df['inputflow'].iloc[-1]-10000)-(df['outputflow'].iloc[-1]-5000))-0.2*((df['inputflow'].iloc[-1]-10000)-(df['outputflow'].iloc[-1]-5000)))/1000,2)
    avg_input_tds = round(filtered_hourly_data['inputtds'].iloc[-1],2)
    avg_output_tds = round(filtered_hourly_data['outputtds'].iloc[-1],2)

    message = ''
    mode = ''

    last_hour_inputflow = len(df[(df['timestamp']>=(df['timestamp'].iloc[-1] - pd.Timedelta(hours=1)))]['inputflow'].unique())
    last_day_inputflow = len(df[(df['timestamp']>=(df['timestamp'].iloc[-1] - pd.Timedelta(hours=24)))]['inputflow'].unique())
    
    if last_day_inputflow == 1:
        message = "Stopped"
        mode='🔴'
    elif last_hour_inputflow == 1:
        message = "Standby"
        mode = '🟡'
    else:
        message = "Running"
        mode = '🟢'

    return (
    (f'Water Served (kl)', water_served),
    (f'Water Saved (kl)', water_saved),
    f'Current Input TDS (ppm) {avg_input_tds}',
    f'Current Output TDS (ppm) {avg_output_tds}',
    (f'Plant Running Status', mode, message), 
    )

#     return [
#     {'title': 'Water Served (kl)', 'value': water_served, 'max_value': round((df['outputflow']-10000)/1000,2).max(), 'color': '#49F8FA'},
#     {'title': 'Water Saved (kl)', 'value': water_saved, 'max_value': round((0.4*((df['inputflow']-10000)-(df['outputflow']-5000))-0.2*((df['inputflow']-10000)-(df['outputflow']-5000)))/1000,2).max(), 'color':'#04B6FE'},
#     {'title': 'Current Input TDS (ppm)', 'value': avg_input_tds, 'max_value': filtered_hourly_data['inputtds'].max(), 'color':'#80370E'},
#     {'title': 'Current Output TDS (ppm)', 'value': avg_output_tds, 'max_value': filtered_hourly_data['outputtds'].max(), 'color': '#FAB994'},
#     {'title': 'Revenue Generated (in ₹)', 'value': revenue, 'max_value': round((df['outputflow']-10000)/1000,2).max() * 0.25 * 1000, 'color':'#36F72C'},
# ]


def create_dials(df):
    # dial_data = update_dials(df)
    # dial_figures = []
    # for dial in dial_data:
    #     dial_figures.append({
    #         'data': [
    #             go.Indicator(
    #                 mode='number+gauge',
    #                 value=dial['value'],
    #                 title=dial['title'],
    #                 gauge={'axis': {'range': [None, dial['max_value']]},
    #                        'bordercolor':'white',
    #                        'threshold': {
    #                            'line': {'color': 'red', 'width': 4},
    #                            'thickness': 0.75,
    #                            'value': dial['value'],
    #                        },
    #                        'bar':{'color':dial['color']}
    #                 }
    #             )
    #         ], 'layout': go.Layout(height=300, plot_bgcolor='#6E716E', paper_bgcolor='#333333', font=dict(color='#FFFFFF'))
    #     })

    return html.Div([
    html.Div([
        html.Div(id='current-dashboard-inputflow', children=[html.Img(src='static/tap.png', style={'width': '50px', 'height': '50px'}), html.Br(), update_dials(df)[0][0], html.Br(), update_dials(df)[0][1]],
                 style={'display':'inline-block', 'margin':'15px', 'padding':'20px', 'width':'15%', 'height':'45%', 'background-color':'black', 'font-weight':'bold', 'font-size':'20px', 'color':'white', 'text-align': 'center'}),
        html.Div(id='current-dashboard-outputflow', children=[html.Img(src='static/water.png', style={'width': '50px', 'height': '50px'}), html.Br(), update_dials(df)[1][0], html.Br(), update_dials(df)[1][1]],
                 style={'display':'inline-block', 'margin':'15px', 'padding':'20px', 'width':'15%', 'height':'45%', 'background-color':'black', 'font-weight':'bold', 'font-size':'20px', 'color':'white', 'text-align': 'center'}),
        html.Div(id='current-dashboard-inputtds', children=[html.Img(src='static/inputtds.png', style={'width': '50px', 'height': '50px'}), html.Br(), update_dials(df)[2]],
                 style={'display':'inline-block', 'margin':'15px', 'padding':'20px', 'width':'15%', 'height':'40%', 'background-color':'black', 'font-weight':'bold', 'font-size':'20px', 'color':'white', 'text-align': 'center'}),
        html.Div(id='current-dashboard-outputtds', children=[html.Img(src='static/outputtds.png', style={'width': '50px', 'height': '50px'}), html.Br(), update_dials(df)[3]],
                 style={'display':'inline-block', 'margin':'15px', 'padding':'20px', 'width':'15%', 'height':'40%', 'background-color':'black', 'font-weight':'bold', 'font-size':'20px', 'color':'white', 'text-align': 'center'}),
        html.Div(id='revenue-generated', children=[update_dials(df)[4][0], html.Br(), html.Br(), html.Span(update_dials(df)[4][1], style={'font-size': '30px'}), html.Br(), update_dials(df)[4][2]],
                 style={'display':'inline-block', 'margin':'15px', 'padding':'16px', 'width':'15%', 'height':'35%', 'background-color':'black', 'font-weight':'bold', 'font-size':'20px', 'color':'white', 'text-align': 'center'}),        
    ], style={'margin':'20px 0', 'text-align': 'center'}),
], style={'background-color':'#6E716E'})


def create_table_chart(df):
    # Create the table data
    water_served = round((df['outputflow'].iloc[-1]-10000)/1000,2)
    revenue = round(0.25 * water_served * 1000,2)

    daily_data = filter_data_daily(str(df['timestamp'].max() - pd.Timedelta(days=15)), str(df['timestamp'].max()))
    daily_water_served = int((daily_data['outputflow'].iloc[-1]-10000) / 20)

    table_data = {
        'Plant Details': [
            'Site Name: Gandhipura',
            'Capacity of Plant: Your Plant Capacity',
            'Technology: CDI Technology',
            'Population: 2xxxx',
            f'Impact Reached: {daily_water_served * 4}',
            f'Revenue Generated (in ₹): {revenue}'
        ]
    }

    # Create table rows with separator border lines
    table_rows = [html.Tr(html.Td(detail, style={'borderBottom': '1px solid #FFFFFF', 'padding': '20px', 'color': '#FFFFFF', 'font-size': '20px', 'font-weight': 'bold', 'text-align': 'center'})) for detail in table_data['Plant Details']]

    # Create the table
    table = html.Div([
        html.H3('Plant Details'),
        html.Table(
            # Table body
            [html.Tbody(table_rows)],
            style={'width':'100%', 'backgroundColor': '#333333'}
        )
    ], style={'padding': '10px', 'margin': '10px', 'width': '90%'})

    # Create combined chart
    fig = go.Figure()
    
    # Add grouped bar chart
    fig.add_trace(
        go.Bar(x=daily_data['timestamp'], y=daily_data['inputflow'] / 1000, name='Input Flow', marker=dict(color='#04B6FE')),
    )
    fig.add_trace(
        go.Bar(x=daily_data['timestamp'], y=daily_data['outputflow'] / 1000, name='Output Flow', marker=dict(color='#49F8FA')),
    )
    
    # Add line chart
    fig.add_trace(
        go.Scatter(x=daily_data['timestamp'], y=daily_data['outputtds'], yaxis='y2', name='Output TDS', mode='lines', marker=dict(color='#FAB994', size=20), line=dict(width=3)),
    )

    fig.update_layout(height=500, showlegend=True,
                      title='Daily Water Input and Output Flow with Average Output TDS',
                      xaxis=dict(title='Timestamp', tickfont=dict(size=14), color='#FFFFFF', showline=True, linecolor='white', linewidth=3),
                      yaxis=dict(title='Water Volume (in kl)', side='left', showgrid=False, showline=True, tickfont=dict(size=12), color='#FFFFFF', linecolor='white', linewidth=3),
                      yaxis2=dict(title='Output TDS (in ppm)', overlaying='y', side='right', range=[daily_data['outputtds'].min(), daily_data['outputtds'].max()], showgrid=False, showline=True, tickfont=dict(size=12), color='#FFFFFF', linecolor='white', linewidth=3),
                      plot_bgcolor='#333333', paper_bgcolor='#333333', font=dict(color='#FFFFFF'),
                      legend=dict(
                                    orientation="h",  # "h" for horizontal, "v" for vertical
                                    x=0.5,  # Position of the legend along the x-axis (0 to 1)
                                    y=1.1)
                     )
    
    return html.Div([
        # Plant details table
        html.Div([
            table
        ], style={'background-color': '#6E716E', 'float': 'left', 'width': '50%'}),

        # Combined chart
        html.Div([
            dcc.Graph(id='combined-chart', figure=fig)
        ], style={'float': 'left', 'width': '50%'})
    ])



