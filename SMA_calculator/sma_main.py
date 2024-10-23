from warnings import filterwarnings
filterwarnings(action="ignore")
import pandas as pd
import plotly.express as px
import requests
from helper_code import wrangle, MovingAverageCalculator
from dash import Dash, dcc, callback, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from datetime import datetime, timedelta

# url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo'
# r = requests.get(url)
# dat = r.json()


data = wrangle("MTN.json",key="Time Series (Daily)")
df_train = data['train']
# output = mac.moving_averages(5)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
        dcc.Dropdown(id="period_selection",options=[i for i in range(3, 11)], value=3),
        dcc.Dropdown(id="type_selection", options=['open', 'low', 'high', 'close'], value='open'),
        dcc.Graph(id="figure1")],
            width=8),
        # dbc.Col([
        #     dcc.DatePickerSingle(min_date_allowed=str(datetime.today()-timedelta(days=30))[:11], max_date_allowed=str(datetime.today())[:11]),
        #     dcc.DatePickerSingle(min_date_allowed=str(datetime.today()-timedelta(days=30))[:11], max_date_allowed=str(datetime.today())[:11])
        # ])
    ])
])

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
