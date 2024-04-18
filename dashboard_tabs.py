import dash
import dash_html_components as html
from dash import dcc
from dash.dependencies import Input, Output
from table_layout import table_layout, update_small_boxes_callback, update_table_callback
from dashboard import create_charts, update_charts_callback, update_small_boxes_dashboard_callback
from get_data import fetch_data_from_api
from data_processing import filter_data
import pandas as pd

df = pd.read_csv('data.csv')

# Initialize Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div([
    
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
    update_small_boxes_callback(app),
    update_table_callback(app),
    update_small_boxes_dashboard_callback(app),
    update_charts_callback(app)
    
])

# Callback to switch tabs
@app.callback(
    Output('tabs', 'value'),
    [Input('table-button', 'n_clicks')]
)
def switch_tabs(n_clicks):
    if n_clicks:
        return 'dashboard-tab'
    return 'table-tab'

if __name__ == '__main__':
    app.run(debug=True)
