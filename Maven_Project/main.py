from dash import Dash, html,callback, dcc, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
df = pd.read_csv("monthly_sales.csv")
cd = pd.read_csv("cleaned_data.csv")
locations = list(cd.store_location.unique())
locations_totals = cd.groupby("store_location").agg({
    "sales":"sum"
    }
)
total_sales_by_category = cd.groupby(["product_category", "product_type"])["sales"].sum().reset_index().set_index("product_category")
sales_by_category = total_sales_by_category.sort_values(by='sales', ascending=True)
sales_by_type = cd.groupby(["store_location","product_category", "product_type"])["sales"].sum().reset_index()
type_sales = sales_by_type.groupby(["store_location","product_type"])["sales"].sum().unstack().T

app = Dash(__name__, external_stylesheets=[dbc.themes.YETI],
           meta_tags=[{'name':'viewport', 'content':'width-device-width, initial-scale=1.0'}])
fig_sales = px.histogram(
    y=sales_by_category["product_type"][16:],
    x=sales_by_category["sales"][16:],
    labels = {"y":"Products"},
    width=700,
    height=700,
    title= "Top selling Products"
    )
fig_sales.update_traces(showlegend=False, hovertemplate="<br>".join(([
        "Revenue: %{x:$, .2f}"
])))
# card_intro = dbc.Card([
#     dbc.CardImg(src="/static/images/intro_photo_one.jpeg", top=True),
# ]
# )
card_sales_fig = dbc.Card(
    dbc.CardImg(src='static/images/MR.png', top=True)
)
card_sales_prop = dbc.Card(
    dbc.CardImg(src='static/images/plot_2.png', top=True)
)
card_summary = dbc.Card([
    dbc.CardBody(
        [html.H2("Introduction")
        ]
    )
]
)



app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H1("Maven Roasters Analytics Report for January to June 20xx", className="text-center text-primary, mb-4"),
            width=12, id="title"
        )
    ]),
    dbc.Row([
        html.Div([html.Img(src="/static/images/intro_photo_one.jpeg",
                           style={
                               "height": "80px",
                               "width": "auto",
                               "margin-bottom": "30px",
                           },
            )]),
    ]
    ),
    dbc.Row([
        dbc.Col(card_sales_fig, width=6),
        dbc.Col(card_sales_prop, width=6)
    ]),
    dbc.Row(
        [   dbc.Col(dbc.Card(
                dbc.CardBody([
                    html.Div(
                        children='Monthly Sales by store.', id="store_name"),
                    dcc.Dropdown(options=locations, id="loc_selection", value="Astoria"),
                    dcc.Graph(id="Rev_per_store(Month)", hoverData={})
                ], )
            ), width={"size":6}),
            dbc.Col(dbc.Card(
                dbc.CardBody([
            html.Div(children="Revenue by product(store)", id="store_location"),
            dcc.Dropdown(options=locations, id="location_selection", value="Astoria"),
            dcc.Graph(id="Rev_by_product(store)", hoverData={})
                ])
            ), width={"size":5}),

        ],

    ),
    dbc.Row([
        dbc.Col(
            [html.Div(children="Sales by product type"),
             dcc.Graph(figure=fig_sales)]
        ),
    ])
        ], fluid=True)

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

@callback(
Output(component_id="Rev_by_product(store)", component_property="figure"),
    Output(component_id="store_location", component_property="children"),
    Input(component_id="location_selection", component_property="value"),
)
def restaurant_product_revenue(btn_selected):
     vals = type_sales[btn_selected].sort_values(ascending=False).to_dict()

     prod = list(vals.keys())
     price = list(vals.values())
     figure=px.histogram(
        data_frame= type_sales,
        x=prod[:10],
        y=price[:10],
        labels={"x":"Product", "y":"Revenue "},width=700, height=700,
        opacity=0.6, title=f"Top Products sold in {btn_selected}",orientation="v")
     return figure, btn_selected

if __name__ == '__main__':
    app.run(debug=True, port=7000)
print(locations_totals["sales"].sum())