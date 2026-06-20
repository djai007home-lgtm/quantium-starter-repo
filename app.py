import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# 1. Initialize the Dash app
app = Dash(__name__)

# 2. Load the cleaned data you generated in Task 2
df = pd.read_csv("./formatted_output.csv")

# 3. Sort the data by date so the line chart reads left-to-right correctly
df = df.sort_values(by="date")

# 4. Create the Plotly line chart
fig = px.line(
    df,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time",
    labels={"date": "Date", "sales": "Total Sales ($)"}
)

# 5. Define what the webpage looks like (HTML layout)
app.layout = html.Div(children=[
    html.H1(
        children="Pink Morsel Sales Visualiser",
        style={"textAlign": "center", "fontFamily": "Arial"}
    ),

    dcc.Graph(
        id="sales-line-chart",
        figure=fig
    )
])

# 6. Run the local web server
if __name__ == "__main__":
    app.run(debug=True)