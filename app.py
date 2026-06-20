import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# 1. Initialize the Dash app
app = Dash(__name__)

# 2. Load and sort the data cleanly by date
df = pd.read_csv("./formatted_output.csv")
df = df.sort_values(by="date")

# 3. Create interactive CSS classes for our buttons (Hover and Active Click states)
# This injects raw CSS into the webpage header so hover triggers correctly
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            /* Base style for all filter buttons */
            .filter-btn {
                padding: 10px 24px;
                font-size: 16px;
                font-weight: bold;
                background-color: #1e293b;
                color: #ffffff;
                border: 2px solid #38bdf8;
                border-radius: 6px;
                cursor: pointer;
                transition: all 0.2s ease-in-out;
            }

            /* What happens when you HOVER your mouse over the button */
            .filter-btn:hover {
                background-color: #334155;
                border-color: #7dd3fc;
                transform: translateY(-1px); /* Slight lift effect */
            }

            /* What happens the exact millisecond you CLICK the button down */
            .filter-btn:active {
                background-color: #38bdf8;
                color: #0f172a;
                transform: translateY(1px);  /* Slight push-down effect */
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# 4. Define the visual layout of the webpage
app.layout = html.Div(
    style={
        "backgroundColor": "#0f172a",  # Deep charcoal background
        "color": "#ffffff",  # Ultra-bright white text
        "fontFamily": "Segoe UI, Arial, sans-serif",
        "padding": "40px",
        "minHeight": "100vh"
    },
    children=[
        # Main Header
        html.H1(
            children="Pink Morsel Sales Visualiser",
            style={
                "textAlign": "center",
                "marginBottom": "10px",
                "color": "#38bdf8",  # Electric blue header text
                "fontSize": "36px",
                "fontWeight": "bold"
            }
        ),

        # Subtitle
        html.P(
            children="Click a button below to filter the transaction data by region.",
            style={
                "textAlign": "center",
                "color": "#e2e8f0",  # High contrast light grey
                "fontSize": "18px",
                "marginBottom": "30px"
            }
        ),

        # Container for the Interactive Filter Buttons
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "center",
                "gap": "15px",
                "marginBottom": "40px"
            },
            children=[
                html.Button("North", id="btn-north", n_clicks=0, className="filter-btn"),
                html.Button("East", id="btn-east", n_clicks=0, className="filter-btn"),
                html.Button("South", id="btn-south", n_clicks=0, className="filter-btn"),
                html.Button("West", id="btn-west", n_clicks=0, className="filter-btn"),
                html.Button("All Regions", id="btn-all", n_clicks=0, className="filter-btn"),
            ]
        ),

        # The Graph Component
        html.Div(
            style={
                "backgroundColor": "#1e293b",
                "padding": "20px",
                "borderRadius": "12px",
                "border": "1px solid #334155"
            },
            children=[
                dcc.Graph(id="sales-line-chart")
            ]
        )
    ]
)


# 5. Interactive Callback Logic
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("btn-north", "n_clicks"),
    Input("btn-east", "n_clicks"),
    Input("btn-south", "n_clicks"),
    Input("btn-west", "n_clicks"),
    Input("btn-all", "n_clicks"),
    prevent_initial_call=False
)
def update_graph(n_north, n_east, n_south, n_west, n_all):
    from dash import callback_context
    ctx = callback_context

    if not ctx.triggered:
        selected_region = "all"
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        selected_region = button_id.replace("btn-", "")

    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["region"] == selected_region]

    fig = px.line(
        filtered_df,
        x="date",
        y="sales",
        title=f"Pink Morsel Sales Over Time — {selected_region.upper()}",
        labels={"date": "Date", "sales": "Total Sales ($)"}
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1e293b",
        plot_bgcolor="#1e293b",
        font_color="#ffffff",
        title_font_color="#38bdf8"
    )

    return fig


# 6. Run the web server
if __name__ == "__main__":
    app.run(debug=True)