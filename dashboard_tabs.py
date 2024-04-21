import dash
# import dash_html_components as html
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from table_layout import table_layout, update_small_boxes_callback, update_table_callback
from dashboard import create_charts, update_charts_callback, update_small_boxes_dashboard_callback
from get_data import fetch_data_from_api
from data_processing import preprocess_data, filter_data
import pandas as pd

df = preprocess_data()

# Initialize Dash app
dashboard_app = dash.Dash(__name__)

# Define app layout
dashboard_app.layout = html.Div([

    # Header with logos
    html.Div([
        html.Img(src="static/iccw_logo.png", style={'height':'80px', 'width':'auto', 'float':'left'}),
        html.H1("Gandhipura Drinking Water Kiosk Dashboard", style={'text-align':'center', 'flex-grow':'1', 'color':'white'}),
        html.Img(src="static/water dashboard.png", style={'height':'80px', 'width':'auto', 'float':'right'}),
     ], style={'display':'flex', 'justify-content':'space-between', 'align-items':'center', 'padding':'20px', 'background-color':'#000000', 'border-bottom':'1px solid #ddd'}),
    
    # Tabs for dashboard and table
    dcc.Tabs(id='tabs', value='table-tab', children=[

        # Table tab  
        dcc.Tab(label='Table', value='table-tab', children=[
            table_layout()
        ]),
        
        # Dashboard tab
        dcc.Tab(label='Dashboard', value='dashboard-tab', children=[
            create_charts(),
            
            # Navigation button
            html.Div([
                html.Button('Go to Table', id='table-button', n_clicks=0, 
                            style={'display':'block', 'margin':'20px auto', 'padding':'10px 20px', 
                                   'font-size':'16px', 'background-color':'#007BFF', 'color':'#fff', 
                                   'border':'none', 'border-radius':'4px', 'cursor':'pointer'})
            ], style={'text-align':'center'})
        ]),
        
    ]),
    
    # Callbacks
    update_small_boxes_callback(dashboard_app),
    update_table_callback(dashboard_app),
    update_small_boxes_dashboard_callback(dashboard_app),
    update_charts_callback(dashboard_app)
    
])

# Callback to switch tabs
@dashboard_app.callback(
    Output('tabs', 'value'),
    [Input('table-button', 'n_clicks')]
)
def switch_tabs(n_clicks):
    if n_clicks:
        return 'dashboard-tab'
    return 'table-tab'

if __name__ == '__main__':
    dashboard_app.run_server(debug=True)
