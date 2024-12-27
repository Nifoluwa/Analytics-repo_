import json
from warnings import filterwarnings
filterwarnings(action="ignore")
import pandas as pd
import plotly.express as px
import requests
import os
from dotenv import load_dotenv
from helper_code import wrangle, MovingAverageCalculator, stock_ticker
from dash import Dash, dcc, callback, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from datetime import datetime, timedelta
api_key = os.getenv("API_KEY")
#api_base_url = os.getenv("API_BASE_URL")
#api_url = f"{api_base_url}={api_key}"
#load_dotenv()


# API call/calls go/goes here........................................
data = wrangle(filename="MTN.json",key="Time Series (Daily)")
df_train = data['train']

#---------------------------------------------------------------
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
        dcc.Dropdown(id="period_selection",options=[i for i in range(3, 11)], value=3, clearable=False),
        dcc.Dropdown(id="type_selection", options=['open', 'low', 'high', 'close'], value='open', clearable=False),
        dcc.Store(id='query_data', storage_type="session"),
        dcc.Graph(id="figure1")],
            width=6),
        dbc.Col([
            dcc.Dropdown(id='data_selection', options=['NVDA', 'AAPL', 'MSFT', 'SONY', 'TSLA', 'IBM', 'META'], value='AAPL', clearable=True)],
            width=3),
        dbc.Col([
            dcc.DatePickerSingle(min_date_allowed=str(datetime.today()-timedelta(days=30))[:11], max_date_allowed=str(datetime.today())[:11]),
            dcc.DatePickerSingle(min_date_allowed=str(datetime.today()-timedelta(days=30))[:11], max_date_allowed=str(datetime.today())[:11])
        ])
    ])
])


@callback(Output(component_id='query_data', component_property="data"),
    Input(component_id='data_selection', component_property='value'))
def ticker(symbol):
    API_BASE_URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey={api_key}"
    r = requests.get(API_BASE_URL)
    data = r.json()
    output = wrangle(file=data, key="Time Series (Daily)")
    df_train = output['train']
    json_data = df_train.to_json()
    file_path = f"{symbol}.json"
    with open(file_path, "w") as f:
        json.dump(json_data, f)
    return json_data

# data = wrangle(ticker())
# df_train = data['train']

@callback( Output(component_id="figure1", component_property="figure"),
    Input(component_id="period_selection", component_property="value"),
    Input(component_id='type_selection', component_property='value'),
         )
def main(dpdn_option, type_selection):
    mac = MovingAverageCalculator(df_train)
    output = mac.moving_averages(dpdn_option, type_selection)
    df = output["Data"]
    sell_dates, sell_values, buy_dates, buy_values = (output['Sell_dates'], output['Sell_values'],
                                                      output['Buy_dates'], output['Buy_values'])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df[type_selection], name="mkt_price"))
    fig.add_trace(go.Scatter(x=df.index, y=df[df.columns[-1]], name=f"{df.columns[-1]}"))
    fig.add_trace(go.Scatter(x=buy_dates, y=buy_values, mode="markers", name="Buy"))
    fig.add_trace(go.Scatter(x=sell_dates, y=sell_values, mode="markers", name="Sell"))
    return fig


if __name__ == "__main__":
    app.run(debug=True)
