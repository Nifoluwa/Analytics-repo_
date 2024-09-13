from dash import Dash, html, dash_table, callback, dcc, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
df = pd.read_csv("monthly_sales.csv")
cd = pd.read_csv("cleaned_data.csv")
locations = list(cd.store_location.unique())
locations_totals = cd.groupby("store_location").agg({
    "sales":"sum"
    }
)
total_sales_by_category = cd.groupby(["product_category", "product_type"])["sales"].sum().reset_index().set_index("product_category")
sales_by_category = total_sales_by_category.sort_values(by='sales', ascending=False)
import numpy as np
app = Dash(__name__, external_stylesheets=[dbc.themes.YETI],
           meta_tags=[{'name':'viewport', 'content':'width-device-width, initial-scale=1.0'}])
fig = px.pie(data_frame=locations_totals,names = locations_totals.index, values=locations_totals.sales, width=500, height=500)
fig_sales = px.bar(
    y=sales_by_category["product_type"][:15],
    x=sales_by_category["sales"][:15],
    color=sales_by_category.product_type[:15],
    labels = {"y":"Products", "x":"Revenue"},
    width=600,
    height=600,
    orientation="h",
    title= "Top selling Products"
    )
fig_sales.update_traces(showlegend=False, hovertemplate="<br>".join(([
        "Revenue: %{x:$, .2f}"
])))
card_intro = dbc.Card([
    dbc.CardImg(src="/static/images/intro_photo_one.jpeg", top=True),
]
)
card_sales_fig = dbc.Card(
    dbc.CardImg(src='static/images/plot_14.png', top=True)
)
card_summary = dbc.Card([
    dbc.CardBody(
        [html.H2("Introduction")
        ]
    )
]
)
card_graph1 = dbc.Card([
        html.Div(children=html.H3('Percentage distribution by store', className="text-center",), style={}),
        dcc.Graph(figure=fig)])



app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H1("Maven Roasters Analytics Report", className="text-center text-primary, mb-4")
        )
    ]),
    dbc.Row([
        dbc.Col(card_intro, width=4,
            ),
        dbc.Col(
            card_summary, width=4
        )
    ]
    ),
    dbc.Row([
        dbc.Col(card_sales_fig, width=6),
    ]),
    dbc.Row(
        [dbc.Col(card_graph1, width=4,
                    ),
        dbc.Col(dbc.Card(
            dbc.CardBody([
        html.Div(
            children='Monthly Sales by store.', id="store_name"),
            dcc.RadioItems(options=locations, id="loc_selection", value="Astoria"),
            dcc.Graph(id="Rev_per_store(Month)", hoverData={})
        ],)
    ), width=6),
    dbc.Row([
        dbc.Col(
            [html.Div(children="Sales by product type"),
             dcc.Graph(figure=fig_sales)]
        )
    ])])])

@callback(
    Output(component_id="Rev_per_store(Month)", component_property="figure"),
    Output(component_id="store_name", component_property="children"),
    Input(component_id="loc_selection", component_property="value"),

)
def update_graph(btn_selected):
    figure=px.histogram(
        data_frame= cd,
        x=cd[cd["store_location"] == btn_selected]["month"].unique(),
        y=cd[cd["store_location"] == btn_selected].groupby("month")["sales"].sum(),
        labels={"x":"Month", "y":"Revenue", "pattern_shape":"Months"},width=700, height=700,
        pattern_shape=cd.month.unique(), opacity=0.6, title=f"Monthly sales for {btn_selected}",)
    figure.update_traces(showlegend=False, hovertemplate="<br>".join(([
        "Month: %{x:$, .2f}",
        "Revenue: %{y:.2f}"
    ])))

    return figure, btn_selected

def product_categories(btn_selected):
    pass
if __name__ == '__main__':
    app.run(debug=True)

print(total_sales_by_category.sort_values(by="sales", ascending=False))
print(cd.columns)