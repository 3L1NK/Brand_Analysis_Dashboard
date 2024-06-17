# import packages
from dash import Dash, html, dcc, callback, Output, Input, clientside_callback, State, ALL, ctx, dash_table
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container
import plotly.graph_objs as go
import math
from datetime import datetime
from assets.styles import NAVBAR_STYLE, LAYOUT_STYLE, HEADER_TITLE_STYLE

# inital variable for neutrogena
df_neutrogena = pd.read_csv('./reddit_sentiment/neutrogena.csv')

# components
navbar = dbc.Navbar(
    dbc.Container(
      children=[
        html.H4(children="Brand Sentiment Analysis", style=HEADER_TITLE_STYLE)
      ],
      fluid=True
    ),
    color="dark",
    dark=True,
    class_name="navbar",
    style=NAVBAR_STYLE
)

pie_chart_container = dbc.Container(
  children=[
    "pie charts"
  ]
)

sentiment_plot_container = dbc.Container(
  children=[
    "sentiment line plot"
  ]
)

# initialise the dash application
app = dash.Dash(
  external_stylesheets=[dbc.themes.BOOTSTRAP],
  suppress_callback_exceptions=True
)

# app layout
app.layout = dbc.Container(
  children=[
    navbar,
    pie_chart_container,
    sentiment_plot_container
  ],
  fluid=True,
  style=LAYOUT_STYLE,
)

# running the dashboard locally on http://127.0.0.1:8050/
if __name__ == '__main__':
  app.run(debug=True)