import dash
# import dash_html_components as html
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from table_layout import table_layout, update_table_callback, view_charts_callback
# from dashboard import create_charts, update_charts_callback, update_small_boxes_dashboard_callback, operations_mode
from information import create_widgets
from get_data import fetch_data_from_api
from data_processing import preprocess_data, filter_data
import pandas as pd
import os

df = preprocess_data()

# Initialize Dash app
dashboard_app = dash.Dash(__name__)

# Define app layout
dashboard_app.layout = html.Div([

    # Header with logos
    html.Div([
        html.Img(src="static/logo.png", style={'height':'90px', 'width':'auto', 'float':'left'}),
        html.H1("Water Kiosk", style={'text-align':'center', 'flex-grow':'1', 'color':'#010738'}),
        html.H3("CDI Technology", style={'text-align':'center', 'flex-grow':'1', 'color':'#010738'}),
        html.Img(src="static/sponsor_logo.png", style={'height':'130px', 'width':'auto', 'float':'right'}),
     ], style={'display':'flex', 'justify-content':'space-between', 'align-items':'center','background-color':'#f5f5f5', 'padding':'2px'}),

    
    # Tabs for dashboard and table
    # dcc.Tabs(id='tabs', value='table-tab', children=[

    #     # Table tab  
    #     dcc.Tab(label='Table', value='table-tab', children=[
    #         table_layout(df)
    #     ]),
        
    #     # Dashboard tab
    #     dcc.Tab(label='Dashboard', value='dashboard-tab', children=[
    #         create_charts(df),
            
    #         # Navigation button
    #         html.Div([
    #             html.Button('Go to Table', id='table-button', n_clicks=0, 
    #                         style={'display':'block', 'margin':'20px auto', 'padding':'10px 20px', 
    #                                'font-size':'16px', 'background-color':'#007BFF', 'color':'#fff', 
    #                                'border':'none', 'border-radius':'4px', 'cursor':'pointer'})
    #         ], style={'text-align':'center'})
    #     ]),
        
    # ]),
    html.Div([
        # create_charts(df)
        create_widgets(df)
    ]),

    # html.Div([
    #     table_layout(df)
    # ]),
    
    # Callbacks
    # update_small_boxes_callback(dashboard_app, df),
    # update_table_callback(dashboard_app),
    # view_charts_callback(dashboard_app),
    # update_small_boxes_dashboard_callback(dashboard_app, df),
    # operations_mode(dashboard_app),
    # update_charts_callback(dashboard_app)
    
])

# Callback to switch tabs
# @dashboard_app.callback(
#     Output('tabs', 'value'),
#     [Input('table-button', 'n_clicks')]
# )
# def switch_tabs(n_clicks):
#     if n_clicks:
#         return 'dashboard-tab'
#     return 'table-tab'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4000))
    dashboard_app.run(host='0.0.0.0', port=port)