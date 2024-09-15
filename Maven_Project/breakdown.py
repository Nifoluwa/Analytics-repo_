import pandas as pd
from warnings import filterwarnings
filterwarnings(action="ignore")

data = pd.read_excel("Data.xlsx")

data["sales"] = data["transaction_qty"] * data["unit_price"]
locations = data.groupby("store_location").agg({
    "sales":"sum",
    "transaction_id":"count"
    }
)

data["year"], data["month"], data["day"] = data["transaction_date"].dt.year,data["transaction_date"].dt.month_name(),data["transaction_date"].dt.day_name()
data["hour"] = [i.hour for i in data.transaction_time]
order = ["January", "February", "March", "April", "May", "June"]
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
sales_by_month = data.groupby("month")["sales"].sum().T[order]
sales_by_month_individual = data.groupby(["store_location", "month"])["sales"].sum().unstack()[order]
product_lines = data.groupby("product_category")["sales"].sum()
category_lines = data.groupby("product_category")["product_detail"].count()
sales_by_type = data.groupby(["store_location","product_category", "product_type"])["sales"].sum().reset_index()
type_sales = sales_by_type.groupby(["store_location","product_type"])["sales"].sum().unstack().T
sales_per_day = data.groupby(["store_location","day"])["sales"].sum().unstack()[day_order].T
sales_by_hour = data.groupby(["store_location", "hour"])["sales"].sum().unstack().T
visits_by_hour =  data.groupby("store_location")["hour"].value_counts().reset_index().set_index("store_location").sort_values(by="hour")
total_sales_by_category = data.groupby(["product_category", "product_type"])["sales"].sum().reset_index().set_index("product_category")
product_by_category = data.groupby("product_category")["product_type"].value_counts().reset_index()









