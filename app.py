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

# inital variable for neutrogena
df_neutrogena = pd.read_csv('./reddit_sentiment/neutrogena.csv')

# components

# initialise the dash application
app = dash.Dash(
  external_stylesheets=[dbc.themes.BOOTSTRAP],
  suppress_callback_exceptions=True
)

# app layout
app.layout = dbc.Container(children=
    ['test'],
    fluid=True,
)

# running the dashboard locally on http://127.0.0.1:8050/
if __name__ == '__main__':
  app.run(debug=True)