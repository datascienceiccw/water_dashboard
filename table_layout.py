from dash import html, dcc, callback_context
import dash
from dash.dependencies import Input, Output, State
from data_processing import filter_data, preprocess_data, filter_data_daily, filter_data_weekly, filter_data_monthly
import pandas as pd

# Global variable to store the filtered dataframe
filtered_df = None

def table_layout(df):
    return html.Div([
        # Date selection
        html.Div([
            html.Div([
                html.Label('From Date'),
                dcc.DatePickerSingle(
                    id='table-from-date-picker',
                    date=df['timestamp'].min(),
                    display_format='DD-MM-YYYY',
                    style={'width':'100%', 'padding':'10px'}
                )
            ], style={'width':'50%', 'display':'inline-block'}),

            html.Div([
                html.Label('To Date'),
                dcc.DatePickerSingle(
                    id='table-to-date-picker',
                    date=df['timestamp'].max(),
                    display_format='DD-MM-YYYY',
                    style={'width':'100%', 'padding':'10px'}
                )
            ], style={'width':'50%', 'display':'inline-block'}),

            html.Div([
                html.Label('Report Type', style={'display':'block', 'margin-bottom':'5px', 'text-align':'right', 'margin-right':'10px'}),
                dcc.Dropdown(
                    id='report-type-dropdown-table',
                    options=[
                        {'label':'Show all', 'value':'show_all'},
                        {'label': 'Daily', 'value': 'daily'},
                        {'label': 'Weekly', 'value': 'weekly'},
                        {'label': 'Monthly', 'value': 'monthly'}
                    ],
                    value='show_all'
                )
            ], style={'width':'30%', 'display':'inline-block', 'text-align':'right'}),
            
            html.Div([
                html.Button('View Charts', id='view-charts-button', n_clicks=0, style={'margin-left': '10px'})
            ], style={'display': 'inline-block'})
        ], style={'margin':'20px 0'}),
        
        # Table
        html.Div([
            html.Table(id='data-table', style={'border':'1px solid #ccc', 'width':'100%', 'border-collapse':'collapse'}),
            html.Div([
                html.Button('Prev', id='prev-button', n_clicks=0, style={'margin':'10px'}),
                html.Button('Next', id='next-button', n_clicks=0, style={'margin':'10px'})
            ], style={'text-align': 'center'})
        ], style={'margin':'20px 0'}),
        
    ], style={'margin':'20px 0'})

# Callback to update table
def update_table_callback(app):
    @app.callback(
        [Output('data-table', 'children'),
         Output('prev-button', 'disabled'),
         Output('next-button', 'disabled')],
        [Input('table-from-date-picker', 'date'),
         Input('table-to-date-picker', 'date'),
         Input('prev-button', 'n_clicks'),
         Input('next-button', 'n_clicks'),
         Input('report-type-dropdown-table', 'value')],
        [State('prev-button', 'n_clicks'),
         State('next-button', 'n_clicks')]
    )
    def update_table(from_date, to_date, prev_clicks, next_clicks, report_type, prev_n_clicks, next_n_clicks):
        global filtered_df

        ctx = callback_context
        button_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

        if report_type == 'daily':
            filtered_df = filter_data_daily(from_date, to_date)
        elif report_type == 'weekly':
            filtered_df = filter_data_weekly(from_date, to_date)
        elif report_type == 'monthly':
            filtered_df = filter_data_monthly(from_date, to_date)
        else:            
            filtered_df = filter_data(from_date, to_date)

        start_index = (prev_n_clicks or 0) * 10
        end_index = (next_n_clicks or 1) * 10

        df_subset = filtered_df.iloc[start_index:end_index]

        return generate_table(df_subset), start_index > 0, len(df_subset) == 10

# Callback to display charts
def view_charts_callback(app):
    @app.callback(
        Output('view-charts-button', 'n_clicks'),
        [Input('data-table', 'children')]
    )
    def view_charts(children):
        return 0 if children else 0

# Function to generate table
def generate_table(dataframe):
    df = dataframe.copy()
    df = df.rename(columns={'inputflow':'input flow (in l)', 'outputflow': 'output flow (in l)', 'inputtds':'input tds (in ppm)', 'outputtds':'output tds (in ppm)'})
    df = df.drop(['output_fluoride', '_id'], axis=1, inplace=False)
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df.columns], style={'border':'1px solid #ccc', 'background-color':'#53E8E8', 'font-weight':'bold'})] +

        # Body
        [html.Tr([
            html.Td(df.iloc[i][col], style={'border':'1px solid #ccc', 'padding':'8px', 'font-size':'16px'}) for col in df.columns
        ], style={'background-color':'#ffffff'}) for i in range(len(df))],
        style={'border-collapse':'collapse', 'width':'100%'}
    )
